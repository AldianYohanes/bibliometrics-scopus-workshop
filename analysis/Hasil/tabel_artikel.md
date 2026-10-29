# Tabel dan gambar artikel (format template workshop)

Dibuat otomatis oleh `Skrip/tabel_template.py` dari `Data/dataset_lolos.csv` (485 paper). Nama kluster **belum diberi**: harus dari membaca dokumen inti (aturan template: interpretasi induktif). TLS = total link strength.

## Gambar 1. Publikasi dan sitasi per tahun

File: `Hasil/gambar1_tren_publikasi.png`

| tahun | dokumen | sitasi |
|---|---|---|
| 2023 | 4 | 2 |
| 2024 | 37 | 844 |
| 2025 | 151 | 1902 |
| 2026 | 293 | 157 |


## Tabel A. Top 10 dokumen berdasarkan sitasi (analisis sitasi)

Sitasi dari OpenAlex (angka global, bukan hanya dari dataset ini).

| Peringkat | Penulis | Judul | Tahun | Sitasi |
|---|---|---|---|---|
| 1 | Ji Lin et al. | AWQ: Activation-aware Weight Quantization for On-Device LLM Compression and Acceleration | 2025 | 273 |
| 2 | Guanqiao Qu et al. | Mobile Edge Intelligence for Large Language Models: A Contemporary Survey | 2025 | 240 |
| 3 | Mingjin Zhang et al. | EdgeShard: Efficient LLM Inference via Collaborative Edge Computing | 2024 | 227 |
| 4 | Othmane Friha et al. | LLM-Based Edge Intelligence: A Comprehensive Survey on Architectures, Applications, Security... | 2024 | 194 |
| 5 | Yue Zheng et al. | A Review on Edge Large Language Models: Design, Execution, and Applications | 2025 | 168 |
| 6 | Fali Wang et al. | A Comprehensive Survey of Small Language Models in the Era of Large Language Models:... | 2025 | 105 |
| 7 | Zheng Lin et al. | Pushing Large Language Models to the 6G Edge: Vision, Challenges, and Opportunities | 2025 | 92 |
| 8 | Xinyuan Zhang et al. | Beyond the Cloud: Edge Inference for Generative Large Language Models in Wireless Networks | 2024 | 77 |
| 9 | Kailai Sun et al. | A review of AI edge devices and lightweight CNN and LLM deployment | 2024 | 72 |
| 10 | Rongjie Yi et al. | EdgeMoE: Empowering Sparse Large Language Models on Mobile Devices | 2025 | 68 |


## Bibliographic coupling

Dari 485 dokumen, 278 punya data referensi; 183 terhubung (≥2 referensi sama) dan membentuk 13 kluster (ukuran: [43, 38, 35, 24, 14, 8, 5, 5, 3, 2, 2, 2, 2]) tanpa ambang. Dengan ambang sitasi dokumen ≥3: 5 kluster (ukuran: [19, 18, 18, 14, 2]); kluster <6 dokumen dibuang, sisa 69 dokumen dalam 4 kluster (ukuran: [19, 18, 18, 14]).

### Tabel B. Top 10 dokumen dalam analisis bibliographic coupling (menurut TLS)

| Peringkat | Publikasi | Sitasi | TLS | Kluster |
|---|---|---|---|---|
| 1 | Wang et al. (2025), Empowering large language models to edge intelligence: A survey of edge... | 47 | 297 | 3 |
| 2 | Friha et al. (2024), LLM-Based Edge Intelligence: A Comprehensive Survey on Architectures,... | 194 | 239 | 2 |
| 3 | Piccialli et al. (2024), Federated and edge learning for large language models | 44 | 232 | 2 |
| 4 | Sun et al. (2024), A review of AI edge devices and lightweight CNN and LLM deployment | 72 | 176 | 3 |
| 5 | Zheng et al. (2025), A Review on Edge Large Language Models: Design, Execution, and Applications | 168 | 175 | 3 |
| 6 | Xu et al. (2024), EdgeLLM: Fast On-Device LLM Inference With Speculative Decoding | 50 | 104 | 3 |
| 7 | Yi et al. (2025), EdgeMoE: Empowering Sparse Large Language Models on Mobile Devices | 68 | 104 | 3 |
| 8 | Qu et al. (2025), Mobile Edge Intelligence for Large Language Models: A Contemporary Survey | 240 | 77 | 1 |
| 9 | Wang et al. (2025), Split Learning Based Cloud-Edge-End Collaborative Model Training in... | 5 | 77 | 1 |
| 10 | Semerikov et al. (2025), Edge intelligence unleashed: a survey on deploying large language models in... | 20 | 75 | 1 |


### Tabel C. Ringkasan kluster bibliographic coupling (kluster ≥6 dokumen)

| Kluster (warna) | Label kluster | Jumlah publikasi | Blok asal | Publikasi representatif |
|---|---|---|---|---|
| 1 (merah) | Edge-cloud collaborative inference and surveys of edge LLM deployment | 19 | {'B': 19} | Qu et al. (2025), Mobile Edge Intelligence for Large Language Models: A Contemporary Survey; Wang et al. (2025), Split Learning Based Cloud-Edge-End Collaborative Model Training in... |
| 2 (hijau) | Edge intelligence surveys, collaborative inference, and hardware acceleration | 18 | {'B': 15, 'A': 2, 'C': 1} | Friha et al. (2024), LLM-Based Edge Intelligence: A Comprehensive Survey on Architectures,...; Piccialli et al. (2024), Federated and edge learning for large language models |
| 3 (biru) | On-device deployment, inference optimisation, and small language models | 18 | {'B': 18} | Wang et al. (2025), Empowering large language models to edge intelligence: A survey of edge...; Sun et al. (2024), A review of AI edge devices and lightweight CNN and LLM deployment |
| 4 (kuning) | Pruning and on-device (federated) fine-tuning | 14 | {'B': 14} | Li et al. (2025), Federated Transfer Learning for On-Device LLMs Efficient Fine Tuning...; Eccles et al. (2025), Mosaic: Composite projection pruning for resource-efficient LLMs |


## Co-citation

Dari 7293 referensi unik, 344 memenuhi ambang 3 sitasi oleh dokumen kita (setelah 10 artefak dibuang), membentuk 5 kluster (ukuran: [128, 95, 58, 57, 6]).

### Tabel D. Top 10 dokumen dengan co-citation dan TLS tertinggi

| Peringkat | Dokumen | Sitasi (oleh dokumen kita) | TLS | Kluster |
|---|---|---|---|---|
| 1 | Touvron (2023), LLaMA: Open and Efficient Foundation Language Models | 13 | 391 | 2 |
| 2 | Ma (2023), LLM-Pruner: On the Structural Pruning of Large Language Models | 15 | 386 | 2 |
| 3 | Shen (2024), Agile-Quant: Activation-Guided Quantization for Faster Inference of LLMs on the... | 10 | 379 | 3 |
| 4 | Kwon (2023), Efficient Memory Management for Large Language Model Serving with PagedAttention | 19 | 369 | 2 |
| 5 | Brown (2020), Language Models are Few-Shot Learners | 16 | 358 | 2 |
| 6 | Liu (2024), LLM-QAT: Data-Free Quantization Aware Training for Large Language Models | 10 | 332 | 2 |
| 7 | Dettmers (2023), QLoRA: Efficient Finetuning of Quantized LLMs | 20 | 306 | 2 |
| 8 | Alizadeh (2024), LLM in a flash: Efficient Large Language Model Inference with Limited Memory | 12 | 299 | 3 |
| 9 | Vaswani (2017), Attention Is All You Need | 12 | 295 | 2 |
| 10 | Ainslie (2023), GQA: Training Generalized Multi-Query Transformer Models from Multi-Head... | 9 | 295 | 2 |


### Tabel E. Kluster co-citation

| Kluster (warna) | Label kluster | Jumlah artikel | Publikasi representatif |
|---|---|---|---|
| 1 (merah) | Edge LLM surveys, collaborative serving, and NLP benchmarks | 128 | Zhang (2024), EdgeShard: Efficient LLM Inference via Collaborative Edge Computing; Zheng (2025), A Review on Edge Large Language Models: Design, Execution, and Applications |
| 2 (hijau) | Quantisation, pruning, and serving efficiency, with foundation models | 95 | Lin (2025), AWQ: Activation-aware Weight Quantization for On-Device LLM Compression and...; Dettmers (2023), QLoRA: Efficient Finetuning of Quantized LLMs |
| 3 (biru) | Mixed background: efficient inference, federated and parameter-efficient tuning, early applications | 58 | Ding (2023), Parameter-efficient fine-tuning of large-scale pre-trained language models; Thirunavukarasu (2023), Large language models in medicine |
| 4 (kuning) | General background: reasoning, edge computing visions, LLM agents, compression basics | 57 | Wei (2022), Chain-Of-Thought Prompting Elicits Reasoning in Large Language Models; Shi (2016), Edge Computing: Vision and Challenges |
| 5 (ungu) | Generative AI in supply chain and operations management | 6 | Jackson (2024), Generative artificial intelligence in supply chain and operations management: a...; AlMahri (2025), Enhancing supply chain visibility with knowledge graphs and large language... |


## Co-word

Dari 2133 kata kunci unik (setelah penggabungan sinonim dan membuang 'large language model' serta 'artificial intelligence'), 68 memenuhi ambang 8 kemunculan, membentuk 3 kluster (ukuran: [24, 23, 21]).

### Tabel F. Top 15 kata kunci dalam analisis co-occurrence

| Peringkat | Kata kunci | Kemunculan | TLS | Kluster |
|---|---|---|---|---|
| 1 | edge computing | 86 | 237 | 2 |
| 2 | on-device inference | 55 | 136 | 3 |
| 3 | small language models | 55 | 151 | 3 |
| 4 | edge deployment | 51 | 127 | 2 |
| 5 | model compression | 51 | 193 | 2 |
| 6 | retrieval-augmented generation | 47 | 109 | 1 |
| 7 | edge devices | 40 | 84 | 3 |
| 8 | energy efficiency | 38 | 125 | 2 |
| 9 | resource-constrained devices | 37 | 132 | 2 |
| 10 | multi-agent systems | 36 | 73 | 1 |
| 11 | agentic ai | 26 | 61 | 1 |
| 12 | inference latency | 26 | 74 | 2 |
| 13 | data privacy | 24 | 71 | 3 |
| 14 | federated learning | 24 | 85 | 3 |
| 15 | llm agents | 24 | 34 | 1 |


### Tabel G. Ringkasan analisis co-word

| Kluster (warna) | Label kluster | Jumlah kata kunci | Kata kunci representatif |
|---|---|---|---|
| 1 (merah) | Agentic AI and RAG for enterprise applications (with an inventory sub-theme) | 24 | retrieval-augmented generation, multi-agent systems, agentic ai, llm agents, inventory management, generative ai, demand forecasting, ai agents |
| 2 (hijau) | Compression and optimisation for edge LLM deployment | 23 | edge computing, model compression, edge deployment, energy efficiency, resource-constrained devices, inference latency, knowledge distillation, on-device large language models |
| 3 (biru) | Small language models and privacy-preserving on-device learning | 21 | small language models, on-device inference, edge devices, federated learning, data privacy, edge ai, parameter-efficient fine-tuning, privacy preservation |


Catatan: warna kluster mengikuti urutan standar VOSviewer (1 merah, 2 hijau, 3 biru, 4 kuning, 5 ungu); cocokkan dengan gambar yang kamu ekspor.
