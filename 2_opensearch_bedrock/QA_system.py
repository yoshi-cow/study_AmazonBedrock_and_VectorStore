import streamlit as st
from langchain_aws import ChatBedrock
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from opensearchpy import OpenSearch
from dotenv import load_dotenv
import boto3
import json
import os

# 環境変数読み込み
load_dotenv()

# bedrockクライアント
br_client = boto3.client("bedrock-runtime", region_name="us-east-1")
dimensions = 256

# opensearch接続
host = os.environ["OPENSEARCH_HOST"]
auth = (os.environ["OPENSEARCH_USER"], os.environ["OPENSEARCH_PASS"])

os_client = OpenSearch(
    hosts = [{'host': host, 'port': 443}],
    http_auth = auth,
    use_ssl = True,
    verify_certs = True,
    ssl_assert_hostname = False,
    ssl_show_warn = False,
    # connection_class = RequestsHttpConnection
)
# インデックス名設定
index_name = "jp-bank-index"


# 質問文のembedding用関数
def embedding_func(question, br_client, dimensions):
    
    # 日本語の文章をエンベディングするためのリクエスト
    request_body = json.dumps(
        {
            "inputText": question,
            "dimensions": dimensions,
            "normalize": True
            })
    response = br_client.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        contentType='application/json',
        accept='application/json',
        body=request_body
    )
    # 結果取得
    response_body = json.loads(response['body'].read())
    embedding = response_body.get('embedding')

    return embedding


# ベクトルストアからの検索用関数と検索結果
def extract_context(os_client, br_client, index_name, question, dimensions):
    # embedding
    vector_for_query = embedding_func(question, br_client, dimensions)
    # query
    search_query = {
        "size": 5,
        "query": {
            "knn": {
                "vector_content": {
                    "vector": vector_for_query, 
                    "k": 3
                }
            }
        }
    }
    results = os_client.search(index=index_name, body=search_query)
    # query結果の抽出
    context = ""
    for hit in results["hits"]["hits"]:
        # print(hit['_source']['content'])
        context += hit['_source']['content']
    
    return context


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
    {"context": RunnablePassthrough(), "question": RunnablePassthrough()}
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
    # ベクトルストアより質問の関連文章抽出
    context = extract_context(os_client, br_client, index_name, question, dimensions)
    response = chain.invoke({"context": context, "question": question})
    st.write(response)