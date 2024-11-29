# study_AmazonBedrock_and_VectorStore
* 生成AIシステム構築用にbedrock及びベクトルストアの構築方法を学ぶ
* "bedrock knowledge base"と"bedrock & opensearch"それぞれでRAGシステムを作り、作成方法を比較する

## RAGシステム内容
* 日銀の「経済・物価情勢の展望」レポートをベクトルストアに保存し、LLMへの質問時に質問と関連する内容を検索してプロンプトに追加する。
 * 該当レポートは、data/jpbank_economy_report.pdf 
* インターフェースは、streamlitを使用
* 実行環境は、AWS Sagemaker Studio コードエディタを使用
* ベクトル化は、"Amazon Titan Text Embeddings"モデルを使用
* 回答は、"anthropic.claude-3-5-sonnet"モデルを使用

## 1. bedrock knowledge baseによるRAGシステムの構築
* 対象ディレクトリ＆ファイル：
  * knowledge_base/
     * knowledge_base_rag.py - kowledge baseに接続して、検索後、プロンプト作成して回答を返すプログラム。
     * set_up_of_knowledge_base.mk - knowledge baseの設定手順
 
* knowledge base利用により以下の利点がある
  1. S3にRAG用の学習ファイルを入れておけば、knowledge base作成時に、ノーコードでファイルを読み込み、チャンクしてベクトルストアを作成してくれる
  2. そのため、ファイルからの文章取り出しから、ベクトルストアの作成までがノーコードでできる
  3. 検索からプロンプト作成までのコードも短くて済む
* 注意点：
  * デフォルトでは、opensearch serverlessを使うが、無料枠もなく、最低料金も高いのでコストかかる
    * → 手動でDBを選択し、pineconeの無料枠を使うなどした方がいい
  * デフォルトで作ると、日本語アナライザーが未設定なので、後で手動で設定が必要
 
<br>
以下knowledge base版回答例-------------

![knowledge_base](https://github.com/user-attachments/assets/e7865487-7bd4-4764-b86c-f209d0f25834)

---------------------

<br>

## 2. bedrock & opensearch serviceによるRAGシステムの構築
* 上記knowledge baseにて作成したRAGと同じシステムを、bedrock・opensearch及びlangchainで再現したもの
* 対象ディレクトリ＆ファイル：
    * 2_opensearch_bedrock/
        * register_data_to_vectordb.ipynb - jpbank_economy_report.pdfの内容をチャンク後ベクトル化してopensearchに登録するためのnotebook
        * QA_system.py - 入力した質問文から関連文書をopensearchから取得後、LLMにコンテキストとして渡して、回答を得るRAG本体（interfaceは、streamlit使用）
* knowledge baseとの比較：
    * 登録から検索まで一つ一つコードを書く必要の無いknowledge baseの方が楽に感じた。
    * 関連文章が段落ごとにまとまっていて、チャンク時に試行錯誤がいらない文書にはknowledge baseが効率的と思われる。

<br>
以下回答例-------------

![opensearch](https://github.com/user-attachments/assets/dd76251e-8b12-4be2-b950-ec0f90d63788)

---------------------
