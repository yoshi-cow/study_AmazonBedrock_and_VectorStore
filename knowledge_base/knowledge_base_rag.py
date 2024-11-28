import streamlit as st
from langchain_aws import ChatBedrock
from langchain_aws.retrievers import AmazonKnowledgeBasesRetriever
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

# 検索手段
retriever = AmazonKnowledgeBasesRetriever(
    knowledge_base_id="AAAAAAAAAA",  # ナレッジベースID
    retrieval_config={"vectorSearchConfiguration": {"numberOfResults": 10}},
)

# プロンプトテンプレート
prompt = ChatPromptTemplate.from_template(
    "以下のcontextに基づき回答してください: {context} / 質問： {question}"
)

# LLM
model = ChatBedrock(
    model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
    # model_id="amazon.titan-text-premier-v1:0",
    model_kwargs={"max_tokens": 1000},
)

# chainの定義（検索→プロンプト作成→LLM呼び出し→結果取得）
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

# フロントエンド作成
st.title("日銀RAG")
question = st.text_input("質問を入力")
button = st.button("質問する")

# ボタンクリックでchain実行結果表示
if button:
    st.write(chain.invoke(question))


# sagemakerからの実行方法は、以下のサイト参照
# https://qiita.com/minorun365/items/f5289163795d5d7b21e2