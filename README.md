# study_AmazonBedrock_and_VectorStore
生成AIシステム構築用にbedrock及びベクトルストアの構築方法を学ぶ

## RAGシステム内容
* 日銀の「経済・物価情勢の展望」レポートをベクトルストアに保存し、LLMへの質問時に質問と関連する内容を検索してプロンプトに追加する。
 * 該当レポートは、data/jpbank_economy_report.pdf 
* インターフェースは、streamlitを使用
* 実行環境は、AWS Sagemaker Studio コードエディタを使用
* "bedrock knowledge base"と"bedrock & opensearch"それぞれでRAGシステムを作り、作成方法を比較する
* ベクトル化は、"Amazon Titan Text Embeddings"モデルを使用
* 回答は、"anthropic.claude-3-5-sonnet"モデルを使用

## 1. bedrock knowledge baseによるRAGシステムの構築
* 対象ディレクトリ＆ファイル：
  * knowledge_base/
    * knowledge_base_rag.py - kowledge baseに接続して、検索後、プロンプト作成して回答を返すプログラム。
    * set_up_of_knowledge_base.mk - knowledge baseの設定手順
 
* knowledge base利用により以下の利点がある
  1. S3にRAG用の学習ファイルを入れておけば、knowledge base作成時に、ノーコードでファイルを読み込み、チャンクしてベクトルストアを作成してくれる
  2. 検索からプロンプト作成までのコードが短くて済む
* 注意点：
  * デフォルトでは、opensearch serverlessを使うが、無料枠もなく、最低料金も高いのでコストかかる
    * → 手動でDBを選択し、pineconeの無料枠を使うなどした方がいい
  * デフォルトで作ると、日本語アナライザーが未設定なので、後で手動で設定が必要
 
<br>
以下回答例
![knowledge_base](https://github.com/user-attachments/assets/e7865487-7bd4-4764-b86c-f209d0f25834)


## 2. bedrock & opensearch serviceによるRAGシステムの構築
