# Knowledge baseの設定手順

1. S3に対象ファイルをセット
2. Amazon Bedrockでナレッジベースを作成
    1. データソースにS3を選択
    2. 対象S3バケットとその中のベクトル化対象ファイルを指定
    3. 埋め込みモデルを選択
    4. ベクトルデータベースを選択
        1. “クイック作成”を選択すると Opensearch Serverlessが自動選択される
        2. “作成したベクトルストア”を選択すると、Amazon OpenSearch Serverless、Amazon Aurora、MongoDB Atlas、Pinecone、または Redis Enterprise Cloudから選べる
  上記ステップにより、RAG用ベクトルストアが自動作成される（ここまで、ノーコードで作成）
3. フロントエンドの実装 - knowledge_base_rag.py　を参照
    1. ナレッジベースIDをコピーしておき、関数での呼び出し時に貼り付ける