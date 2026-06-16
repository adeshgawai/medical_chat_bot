# Action Plan: Fixing Latency and Greeting Issues

Below is the step-by-step implementation plan to fix the chatbot's high latency and enable it to handle conversational greetings.

---

## Step 1: Implement a Query Router (Greeting Handler)
To avoid running the expensive retrieval, evaluation, and web search pipeline for simple greetings or generic conversational queries, we will introduce a **Query Router** at the beginning of the workflow.

### Code Changes Required:
1. **Define the Router Logic in [src/nodes.py](file:///E:/NLP_learning/Projects/RAG/medical_chat_bot/crag-based-chatbot/src/nodes.py):**
   * Create a Pydantic structure for classification:
     ```python
     class RouteQuery(BaseModel):
         datasource: str = Field(
             description="Route the user question to 'medical_rag' or 'general_chat'."
         )
     ```
   * Create a router prompt and chain:
     ```python
     router_prompt = ChatPromptTemplate.from_messages([
         ("system", "You are an expert router. If the user question is a greeting, general chit-chat (e.g., 'hello', 'how are you'), or conversational filler, route it to 'general_chat'. Otherwise, route it to 'medical_rag'."),
         ("human", "{question}")
     ])
     router_chain = router_prompt | llm.with_structured_output(RouteQuery)
     ```
   * Create a routing function:
     ```python
     def route_question(state):
         q = state["question"]
         decision = router_chain.invoke({"question": q})
         if decision.datasource == "general_chat":
             return "general_chat"
         return "medical_rag"
     ```

2. **Update the State Graph in [src/graph.py](file:///E:/NLP_learning/Projects/RAG/medical_chat_bot/crag-based-chatbot/src/graph.py):**
   * Add a conditional edge right after the `START` node:
     ```python
     g.add_conditional_edges(
         START,
         route_question,
         {
             "general_chat": "generate",   # Bypass RAG entirely
             "medical_rag": "retrieve"     # Normal RAG pipeline
         }
     )
     ```

---

## Step 2: Parallelize LLM Calls in Loops (Latency Optimization)
Instead of sequentially calling `llm.invoke` in loops, use LangChain's asynchronous batching capability (`.batch()`). This executes the LLM calls concurrently, reducing wait times by up to **90%**.

### Code Changes Required:
1. **Optimize Document Evaluation in [src/nodes.py](file:///E:/NLP_learning/Projects/RAG/medical_chat_bot/crag-based-chatbot/src/nodes.py#L48):**
   * Rewrite `eval_each_doc` to use batch processing:
     ```python
     def eval_each_doc(state):
         q = state['question']
         docs = state['docs']
         
         if not docs:
             return {"good_docs": [], "verdict": "INCORRECT", "reason": "No documents retrieved."}

         # Batch invoke the LLM for all documents concurrently
         inputs = [{"question": q, "chunk": d.page_content} for d in docs]
         results = doc_eval_chain.batch(inputs)

         scores = [r.score for r in results]
         good = [d for d, r in zip(docs, results) if r.score > LOWER_TH]
         
         # Maintain the rest of the scoring logic...
     ```

2. **Optimize Sentence Filtering in [src/nodes.py](file:///E:/NLP_learning/Projects/RAG/medical_chat_bot/crag-based-chatbot/src/nodes.py#L125):**
   * Rewrite `refine` to use batch processing for sentences:
     ```python
     def refine(state):
         q = state['question']
         # ... existing setup code ...

         context = "\n\n".join(d.page_content for d in docs_to_use).strip()
         strips = decompose_to_sentences(context)
         
         if not strips:
             return {"strips": [], "kept_strips": [], "refined_context": ""}

         # Batch invoke the LLM for all sentences concurrently
         inputs = [{"question": q, "sentence": s} for s in strips]
         results = filter_chain.batch(inputs)

         kept = [s for s, res in zip(strips, results) if res.keep]
         refined_context = "\n".join(kept).strip()

         return {
             "strips": strips,
             "kept_strips": kept,
             "refined_context": refined_context
         }
     ```

---

## Step 3: Refine the Prompt to Handle General Chat
To ensure the LLM doesn't output a medical disclaimer for greetings when routed straight to `generate`, adjust the system instructions.

### Code Changes Required:
* **Update the Prompt Template in [src/prompt.py](file:///E:/NLP_learning/Projects/RAG/medical_chat_bot/crag-based-chatbot/src/prompt.py#L3):**
  ```python
  def prompt_to_llm():
      prompt = PromptTemplate(
          template="""
          You are MediAssist, an expert medical AI assistant.
          
          Guidelines:
          1. If the user's input is a greeting or a general, polite question (e.g. "hello", "how are you", "good morning"), respond politely and helpfully without requiring medical context.
          2. For medical questions, answers must be factual, clear, and based ONLY on the provided Context.
          3. If the Context is empty/insufficient for medical questions, say:
             "I don't have enough information in my medical database to answer that. Please consult a licensed physician."

          Context:
          {refined_context}

          Question: {question}

          Answer:
          """,
          input_variables=['refined_context', 'question']
      )
      return prompt
  ```
