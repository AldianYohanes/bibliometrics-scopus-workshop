# Tabel dan gambar artikel (format template workshop)

Dibuat otomatis oleh `Skrip/tabel_template.py` dari `Data/dataset_lolos.csv` (485 paper). Nama kluster **belum diberi**: harus dari membaca dokumen inti (aturan template: interpretasi induktif). TLS = total link strength.

## Gambar 1. Publikasi dan sitasi per tahun

File: `Hasil/gambar1_tren_publikasi.png`

| tahun | dokumen | sitasi |
|---|---|---|
| 2023 | 4 | 2 |
| 2024 | 37 | 844 |
| 2025 | 153 | 1907 |
| 2026 | 295 | 157 |


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

Dari 489 dokumen, 282 punya data referensi; 184 terhubung (≥2 referensi sama) dan membentuk 12 kluster (ukuran: [55, 38, 38, 18, 14, 5, 5, 3, 2, 2, 2, 2]) tanpa ambang. Dengan ambang sitasi dokumen ≥3: 5 kluster (ukuran: [20, 20, 17, 13, 2]); kluster <6 dokumen dibuang, sisa 70 dokumen dalam 4 kluster (ukuran: [20, 20, 17, 13]).

### Tabel B. Top 10 dokumen dalam analisis bibliographic coupling (menurut TLS)

| Peringkat | Publikasi | Sitasi | TLS | Kluster |
|---|---|---|---|---|
| 1 | Wang et al. (2025), Empowering large language models to edge intelligence: A survey of edge... | 47 | 297 | 1 |
| 2 | Friha et al. (2024), LLM-Based Edge Intelligence: A Comprehensive Survey on Architectures,... | 194 | 239 | 3 |
| 3 | Piccialli et al. (2024), Federated and edge learning for large language models | 44 | 235 | 3 |
| 4 | Sun et al. (2024), A review of AI edge devices and lightweight CNN and LLM deployment | 72 | 176 | 4 |
| 5 | Zheng et al. (2025), A Review on Edge Large Language Models: Design, Execution, and Applications | 168 | 175 | 1 |
| 6 | Xu et al. (2024), EdgeLLM: Fast On-Device LLM Inference With Speculative Decoding | 50 | 104 | 1 |
| 7 | Yi et al. (2025), EdgeMoE: Empowering Sparse Large Language Models on Mobile Devices | 68 | 104 | 1 |
| 8 | Qu et al. (2025), Mobile Edge Intelligence for Large Language Models: A Contemporary Survey | 240 | 80 | 3 |
| 9 | Wang et al. (2025), Split Learning Based Cloud-Edge-End Collaborative Model Training in... | 5 | 77 | 2 |
| 10 | Semerikov et al. (2025), Edge intelligence unleashed: a survey on deploying large language models in... | 20 | 75 | 2 |


### Tabel C. Ringkasan kluster bibliographic coupling (kluster ≥6 dokumen)

| Kluster (warna) | Label kluster | Jumlah publikasi | Blok asal | Publikasi representatif |
|---|---|---|---|---|
| 1 (merah) | Efficient on-device inference on mobile hardware | 20 | {'B': 19, 'A': 1} | Wang et al. (2025), Empowering large language models to edge intelligence: A survey of edge...; Zheng et al. (2025), A Review on Edge Large Language Models: Design, Execution, and Applications |
| 2 (hijau) | Edge LLM surveys and distributed fine-tuning | 20 | {'B': 20} | Wang et al. (2025), Split Learning Based Cloud-Edge-End Collaborative Model Training in...; Semerikov et al. (2025), Edge intelligence unleashed: a survey on deploying large language models in... |
| 3 (biru) | Applied edge intelligence across domains | 17 | {'B': 16, 'C': 1} | Friha et al. (2024), LLM-Based Edge Intelligence: A Comprehensive Survey on Architectures,...; Piccialli et al. (2024), Federated and edge learning for large language models |
| 4 (kuning) | Privacy-preserving and personalised LLMs for IoT | 13 | {'B': 12, 'A': 1} | Sun et al. (2024), A review of AI edge devices and lightweight CNN and LLM deployment; Li et al. (2025), Federated Transfer Learning for On-Device LLMs Efficient Fine Tuning... |


## Co-citation

Dari 7357 referensi unik, 347 memenuhi ambang 3 sitasi oleh dokumen kita (setelah 10 artefak dibuang), membentuk 4 kluster (ukuran: [127, 95, 66, 59]).

### Tabel D. Top 10 dokumen dengan co-citation dan TLS tertinggi

| Peringkat | Dokumen | Sitasi (oleh dokumen kita) | TLS | Kluster |
|---|---|---|---|---|
| 1 | Touvron (2023), LLaMA: Open and Efficient Foundation Language Models | 13 | 392 | 2 |
| 2 | Ma (2023), LLM-Pruner: On the Structural Pruning of Large Language Models | 15 | 387 | 2 |
| 3 | Shen (2024), Agile-Quant: Activation-Guided Quantization for Faster Inference of LLMs on the... | 10 | 380 | 4 |
| 4 | Kwon (2023), Efficient Memory Management for Large Language Model Serving with PagedAttention | 19 | 369 | 2 |
| 5 | Brown (2020), Language Models are Few-Shot Learners | 16 | 359 | 2 |
| 6 | Liu (2024), LLM-QAT: Data-Free Quantization Aware Training for Large Language Models | 10 | 332 | 2 |
| 7 | Dettmers (2023), QLoRA: Efficient Finetuning of Quantized LLMs | 20 | 308 | 2 |
| 8 | Alizadeh (2024), LLM in a flash: Efficient Large Language Model Inference with Limited Memory | 12 | 300 | 4 |
| 9 | Vaswani (2017), Attention Is All You Need | 12 | 297 | 2 |
| 10 | Ainslie (2023), GQA: Training Generalized Multi-Query Transformer Models from Multi-Head... | 9 | 295 | 2 |


### Tabel E. Kluster co-citation

| Kluster (warna) | Label kluster | Jumlah artikel | Publikasi representatif |
|---|---|---|---|
| 1 (merah) | Collaborative edge-cloud LLM serving and its evaluation | 127 | Zhang (2024), EdgeShard: Efficient LLM Inference via Collaborative Edge Computing; Zheng (2025), A Review on Edge Large Language Models: Design, Execution, and Applications |
| 2 (hijau) | Model compression and efficient inference foundations | 95 | Lin (2025), AWQ: Activation-aware Weight Quantization for On-Device LLM Compression and...; Dettmers (2023), QLoRA: Efficient Finetuning of Quantized LLMs |
| 3 (biru) | Shared foundations: reasoning, agents, and supply chain AI | 66 | Wei (2022), Chain-Of-Thought Prompting Elicits Reasoning in Large Language Models; Shi (2016), Edge Computing: Vision and Challenges |
| 4 (kuning) | Mobile inference and decentralised adaptation | 59 | Alizadeh (2024), LLM in a flash: Efficient Large Language Model Inference with Limited Memory; Thirunavukarasu (2023), Large language models in medicine |


## Co-word

Dari 2142 kata kunci unik (setelah penggabungan sinonim dan membuang 'large language model' serta 'artificial intelligence'), 69 memenuhi ambang 8 kemunculan, membentuk 3 kluster (ukuran: [24, 23, 22]).

### Tabel F. Top 15 kata kunci dalam analisis co-occurrence

| Peringkat | Kata kunci | Kemunculan | TLS | Kluster |
|---|---|---|---|---|
| 1 | edge computing | 86 | 239 | 2 |
| 2 | on-device inference | 55 | 138 | 3 |
| 3 | small language models | 55 | 152 | 3 |
| 4 | edge deployment | 52 | 131 | 2 |
| 5 | model compression | 51 | 193 | 2 |
| 6 | retrieval-augmented generation | 47 | 109 | 1 |
| 7 | edge devices | 40 | 85 | 3 |
| 8 | energy efficiency | 39 | 129 | 2 |
| 9 | resource-constrained devices | 37 | 132 | 2 |
| 10 | multi-agent systems | 36 | 73 | 1 |
| 11 | agentic ai | 26 | 61 | 1 |
| 12 | federated learning | 26 | 91 | 3 |
| 13 | inference latency | 26 | 74 | 2 |
| 14 | data privacy | 24 | 71 | 3 |
| 15 | llm agents | 24 | 34 | 1 |


### Tabel G. Ringkasan analisis co-word

| Kluster (warna) | Label kluster | Jumlah kata kunci | Kata kunci representatif |
|---|---|---|---|
| 1 (merah) | Agentic and retrieval-augmented LLMs for business operations | 24 | retrieval-augmented generation, multi-agent systems, agentic ai, llm agents, inventory management, generative ai, demand forecasting, ai agents |
| 2 (hijau) | Model compression and optimisation for edge deployment | 23 | edge computing, edge deployment, model compression, energy efficiency, resource-constrained devices, inference latency, knowledge distillation, on-device large language models |
| 3 (biru) | Small language models and privacy-preserving on-device AI | 22 | on-device inference, small language models, edge devices, federated learning, data privacy, edge ai, parameter-efficient fine-tuning, privacy preservation |


Catatan: warna kluster mengikuti urutan standar VOSviewer (1 merah, 2 hijau, 3 biru, 4 kuning, 5 ungu); cocokkan dengan gambar yang kamu ekspor.
