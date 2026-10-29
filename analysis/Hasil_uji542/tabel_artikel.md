# Tabel dan gambar artikel (format template workshop)

Dibuat otomatis oleh `Skrip/tabel_template.py` dari `Data/dataset_lolos.csv` (485 paper). Nama kluster **belum diberi**: harus dari membaca dokumen inti (aturan template: interpretasi induktif). TLS = total link strength.

## Gambar 1. Publikasi dan sitasi per tahun

File: `Hasil/gambar1_tren_publikasi.png`

| tahun | dokumen | sitasi |
|---|---|---|
| 2023 | 8 | 63 |
| 2024 | 47 | 1361 |
| 2025 | 171 | 1955 |
| 2026 | 316 | 166 |


## Tabel A. Top 10 dokumen berdasarkan sitasi (analisis sitasi)

Sitasi dari OpenAlex (angka global, bukan hanya dari dataset ini).

| Peringkat | Penulis | Judul | Tahun | Sitasi |
|---|---|---|---|---|
| 1 | Ilya Jackson et al. | Generative artificial intelligence in supply chain and operations management: a... | 2024 | 456 |
| 2 | Ji Lin et al. | AWQ: Activation-aware Weight Quantization for On-Device LLM Compression and Acceleration | 2025 | 273 |
| 3 | Guanqiao Qu et al. | Mobile Edge Intelligence for Large Language Models: A Contemporary Survey | 2025 | 240 |
| 4 | Mingjin Zhang et al. | EdgeShard: Efficient LLM Inference via Collaborative Edge Computing | 2024 | 227 |
| 5 | Othmane Friha et al. | LLM-Based Edge Intelligence: A Comprehensive Survey on Architectures, Applications, Security... | 2024 | 194 |
| 6 | Yue Zheng et al. | A Review on Edge Large Language Models: Design, Execution, and Applications | 2025 | 168 |
| 7 | Fali Wang et al. | A Comprehensive Survey of Small Language Models in the Era of Large Language Models:... | 2025 | 105 |
| 8 | Zheng Lin et al. | Pushing Large Language Models to the 6G Edge: Vision, Challenges, and Opportunities | 2025 | 92 |
| 9 | Xinyuan Zhang et al. | Beyond the Cloud: Edge Inference for Generative Large Language Models in Wireless Networks | 2024 | 77 |
| 10 | Kailai Sun et al. | A review of AI edge devices and lightweight CNN and LLM deployment | 2024 | 72 |


## Bibliographic coupling

Dari 542 dokumen, 301 punya data referensi; 201 terhubung (≥2 referensi sama) dan membentuk 14 kluster (ukuran: [46, 42, 38, 20, 15, 14, 8, 5, 3, 2, 2, 2, 2, 2]) tanpa ambang. Dengan ambang sitasi dokumen ≥3: 6 kluster (ukuran: [19, 18, 17, 16, 11, 2]); kluster <6 dokumen dibuang, sisa 81 dokumen dalam 5 kluster (ukuran: [19, 18, 17, 16, 11]).

### Tabel B. Top 10 dokumen dalam analisis bibliographic coupling (menurut TLS)

| Peringkat | Publikasi | Sitasi | TLS | Kluster |
|---|---|---|---|---|
| 1 | Wang et al. (2025), Empowering large language models to edge intelligence: A survey of edge... | 47 | 300 | 1 |
| 2 | Friha et al. (2024), LLM-Based Edge Intelligence: A Comprehensive Survey on Architectures,... | 194 | 241 | 4 |
| 3 | Piccialli et al. (2024), Federated and edge learning for large language models | 44 | 239 | 4 |
| 4 | Sun et al. (2024), A review of AI edge devices and lightweight CNN and LLM deployment | 72 | 179 | 1 |
| 5 | Zheng et al. (2025), A Review on Edge Large Language Models: Design, Execution, and Applications | 168 | 177 | 1 |
| 6 | Xu et al. (2024), EdgeLLM: Fast On-Device LLM Inference With Speculative Decoding | 50 | 106 | 1 |
| 7 | Yi et al. (2025), EdgeMoE: Empowering Sparse Large Language Models on Mobile Devices | 68 | 104 | 1 |
| 8 | Qu et al. (2025), Mobile Edge Intelligence for Large Language Models: A Contemporary Survey | 240 | 80 | 4 |
| 9 | Wang et al. (2025), Split Learning Based Cloud-Edge-End Collaborative Model Training in... | 5 | 77 | 3 |
| 10 | Semerikov et al. (2025), Edge intelligence unleashed: a survey on deploying large language models in... | 20 | 75 | 3 |


### Tabel C. Ringkasan kluster bibliographic coupling (kluster ≥6 dokumen)

| Kluster (warna) | Label kluster | Jumlah publikasi | Blok asal | Publikasi representatif |
|---|---|---|---|---|
| 1 (merah) | [BELUM DIBERI NAMA] | 19 | {'B': 18, 'A': 1} | Wang et al. (2025), Empowering large language models to edge intelligence: A survey of edge...; Sun et al. (2024), A review of AI edge devices and lightweight CNN and LLM deployment |
| 2 (hijau) | [BELUM DIBERI NAMA] | 18 | {'C': 8, 'A+C': 3, 'B': 6, 'A': 1} | Wang et al. (2025), Intelligent data analysis in edge computing with large language models:...; Jackson et al. (2024), Generative artificial intelligence in supply chain and operations management: a... |
| 3 (biru) | [BELUM DIBERI NAMA] | 17 | {'B': 17} | Wang et al. (2025), Split Learning Based Cloud-Edge-End Collaborative Model Training in...; Semerikov et al. (2025), Edge intelligence unleashed: a survey on deploying large language models in... |
| 4 (kuning) | [BELUM DIBERI NAMA] | 16 | {'C': 1, 'B': 15} | Friha et al. (2024), LLM-Based Edge Intelligence: A Comprehensive Survey on Architectures,...; Piccialli et al. (2024), Federated and edge learning for large language models |
| 5 (ungu) | [BELUM DIBERI NAMA] | 11 | {'B': 11} | Li et al. (2025), Federated Transfer Learning for On-Device LLMs Efficient Fine Tuning...; Eccles et al. (2025), Mosaic: Composite projection pruning for resource-efficient LLMs |


## Co-citation

Dari 7904 referensi unik, 365 memenuhi ambang 3 sitasi oleh dokumen kita (setelah 10 artefak dibuang), membentuk 5 kluster (ukuran: [116, 97, 67, 62, 23]).

### Tabel D. Top 10 dokumen dengan co-citation dan TLS tertinggi

| Peringkat | Dokumen | Sitasi (oleh dokumen kita) | TLS | Kluster |
|---|---|---|---|---|
| 1 | Touvron (2023), LLaMA: Open and Efficient Foundation Language Models | 13 | 394 | 2 |
| 2 | Ma (2023), LLM-Pruner: On the Structural Pruning of Large Language Models | 15 | 387 | 2 |
| 3 | Shen (2024), Agile-Quant: Activation-Guided Quantization for Faster Inference of LLMs on the... | 10 | 381 | 4 |
| 4 | Kwon (2023), Efficient Memory Management for Large Language Model Serving with PagedAttention | 19 | 370 | 2 |
| 5 | Brown (2020), Language Models are Few-Shot Learners | 17 | 368 | 2 |
| 6 | Liu (2024), LLM-QAT: Data-Free Quantization Aware Training for Large Language Models | 10 | 334 | 2 |
| 7 | Dettmers (2023), QLoRA: Efficient Finetuning of Quantized LLMs | 20 | 309 | 2 |
| 8 | Vaswani (2017), Attention Is All You Need | 13 | 308 | 2 |
| 9 | Alizadeh (2024), LLM in a flash: Efficient Large Language Model Inference with Limited Memory | 12 | 301 | 4 |
| 10 | Ainslie (2023), GQA: Training Generalized Multi-Query Transformer Models from Multi-Head... | 9 | 296 | 2 |


### Tabel E. Kluster co-citation

| Kluster (warna) | Label kluster | Jumlah artikel | Publikasi representatif |
|---|---|---|---|
| 1 (merah) | [BELUM DIBERI NAMA] | 116 | Zhang (2024), EdgeShard: Efficient LLM Inference via Collaborative Edge Computing; Zheng (2025), A Review on Edge Large Language Models: Design, Execution, and Applications |
| 2 (hijau) | [BELUM DIBERI NAMA] | 97 | Lin (2025), AWQ: Activation-aware Weight Quantization for On-Device LLM Compression and...; Dettmers (2023), QLoRA: Efficient Finetuning of Quantized LLMs |
| 3 (biru) | [BELUM DIBERI NAMA] | 67 | Wei (2022), Chain-Of-Thought Prompting Elicits Reasoning in Large Language Models; Shi (2016), Edge Computing: Vision and Challenges |
| 4 (kuning) | [BELUM DIBERI NAMA] | 62 | Alizadeh (2024), LLM in a flash: Efficient Large Language Model Inference with Limited Memory; Ding (2023), Parameter-efficient fine-tuning of large-scale pre-trained language models |
| 5 (ungu) | [BELUM DIBERI NAMA] | 23 | Wamba (2023), ChatGPT and generative artificial intelligence: an exploratory study of key...; Wamba (2023), Are both generative AI and ChatGPT game changers for 21st-Century operations... |


## Co-word

Dari 2354 kata kunci unik (setelah penggabungan sinonim dan membuang 'large language model' serta 'artificial intelligence'), 80 memenuhi ambang 8 kemunculan, membentuk 2 kluster (ukuran: [45, 35]).

### Tabel F. Top 15 kata kunci dalam analisis co-occurrence

| Peringkat | Kata kunci | Kemunculan | TLS | Kluster |
|---|---|---|---|---|
| 1 | edge computing | 86 | 240 | 1 |
| 2 | on-device inference | 55 | 139 | 1 |
| 3 | small language models | 55 | 153 | 1 |
| 4 | generative ai | 54 | 164 | 2 |
| 5 | edge deployment | 52 | 132 | 1 |
| 6 | retrieval-augmented generation | 52 | 129 | 2 |
| 7 | model compression | 51 | 194 | 1 |
| 8 | inventory management | 49 | 134 | 2 |
| 9 | edge devices | 40 | 85 | 1 |
| 10 | multi-agent systems | 40 | 93 | 2 |
| 11 | energy efficiency | 39 | 130 | 1 |
| 12 | resource-constrained devices | 37 | 132 | 1 |
| 13 | demand forecasting | 36 | 124 | 2 |
| 14 | agentic ai | 29 | 82 | 2 |
| 15 | data privacy | 26 | 82 | 1 |


### Tabel G. Ringkasan analisis co-word

| Kluster (warna) | Label kluster | Jumlah kata kunci | Kata kunci representatif |
|---|---|---|---|
| 1 (merah) | [BELUM DIBERI NAMA] | 45 | edge computing, on-device inference, small language models, edge deployment, model compression, edge devices, energy efficiency, resource-constrained devices |
| 2 (hijau) | [BELUM DIBERI NAMA] | 35 | generative ai, retrieval-augmented generation, inventory management, multi-agent systems, demand forecasting, agentic ai, llm agents, supply chain management |


Catatan: warna kluster mengikuti urutan standar VOSviewer (1 merah, 2 hijau, 3 biru, 4 kuning, 5 ungu); cocokkan dengan gambar yang kamu ekspor.
