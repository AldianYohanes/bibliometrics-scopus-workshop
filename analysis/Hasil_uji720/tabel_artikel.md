# Tabel dan gambar artikel (format template workshop)

Dibuat otomatis oleh `Skrip/tabel_template.py` dari `Data/dataset_lolos.csv` (485 paper). Nama kluster **belum diberi**: harus dari membaca dokumen inti (aturan template: interpretasi induktif). TLS = total link strength.

## Gambar 1. Publikasi dan sitasi per tahun

File: `Hasil/gambar1_tren_publikasi.png`

| tahun | dokumen | sitasi |
|---|---|---|
| 2023 | 6 | 6 |
| 2024 | 57 | 1331 |
| 2025 | 223 | 2331 |
| 2026 | 434 | 226 |


## Tabel A. Top 10 dokumen berdasarkan sitasi (analisis sitasi)

Sitasi dari OpenAlex (angka global, bukan hanya dari dataset ini).

| Peringkat | Penulis | Judul | Tahun | Sitasi |
|---|---|---|---|---|
| 1 | Ji Lin et al. | AWQ: Activation-aware Weight Quantization for On-Device LLM Compression and Acceleration | 2025 | 273 |
| 2 | Guanqiao Qu et al. | Mobile Edge Intelligence for Large Language Models: A Contemporary Survey | 2025 | 240 |
| 3 | Mingjin Zhang et al. | EdgeShard: Efficient LLM Inference via Collaborative Edge Computing | 2024 | 227 |
| 4 | Othmane Friha et al. | LLM-Based Edge Intelligence: A Comprehensive Survey on Architectures, Applications, Security... | 2024 | 194 |
| 5 | Yue Zheng et al. | A Review on Edge Large Language Models: Design, Execution, and Applications | 2025 | 168 |
| 6 | Ying He et al. | Large Language Models (LLMs) Inference Offloading and Resource Allocation in Cloud-Edge... | 2024 | 127 |
| 7 | Lina Bariah et al. | Large Generative AI Models for Telecom: The Next Big Thing? | 2024 | 127 |
| 8 | Minrui Xu et al. | When Large Language Model Agents Meet 6G Networks: Perception, Grounding, and Alignment | 2024 | 105 |
| 9 | Fali Wang et al. | A Comprehensive Survey of Small Language Models in the Era of Large Language Models:... | 2025 | 105 |
| 10 | Zheng Lin et al. | Pushing Large Language Models to the 6G Edge: Vision, Challenges, and Opportunities | 2025 | 92 |


## Bibliographic coupling

Dari 720 dokumen, 413 punya data referensi; 277 terhubung (≥2 referensi sama) dan membentuk 12 kluster (ukuran: [64, 51, 49, 38, 37, 18, 6, 5, 3, 2, 2, 2]) tanpa ambang. Dengan ambang sitasi dokumen ≥3: 5 kluster (ukuran: [28, 25, 25, 22, 3]); kluster <6 dokumen dibuang, sisa 100 dokumen dalam 4 kluster (ukuran: [28, 25, 25, 22]).

### Tabel B. Top 10 dokumen dalam analisis bibliographic coupling (menurut TLS)

| Peringkat | Publikasi | Sitasi | TLS | Kluster |
|---|---|---|---|---|
| 1 | Wang et al. (2025), Empowering large language models to edge intelligence: A survey of edge... | 47 | 385 | 1 |
| 2 | Friha et al. (2024), LLM-Based Edge Intelligence: A Comprehensive Survey on Architectures,... | 194 | 334 | 3 |
| 3 | Piccialli et al. (2024), Federated and edge learning for large language models | 44 | 315 | 3 |
| 4 | Sun et al. (2024), A review of AI edge devices and lightweight CNN and LLM deployment | 72 | 246 | 1 |
| 5 | Zheng et al. (2025), A Review on Edge Large Language Models: Design, Execution, and Applications | 168 | 234 | 1 |
| 6 | Shao et al. (2025), Imp: Highly Capable Large Multimodal Models for Mobile Devices | 11 | 156 | 2 |
| 7 | Xu et al. (2024), EdgeLLM: Fast On-Device LLM Inference With Speculative Decoding | 50 | 141 | 1 |
| 8 | Yi et al. (2025), EdgeMoE: Empowering Sparse Large Language Models on Mobile Devices | 68 | 132 | 1 |
| 9 | Zhang et al. (2024), EdgeTA: Neuron-Grained Scaling of Foundation Models in Edge-Side Retraining | 6 | 108 | 2 |
| 10 | Li et al. (2025), Federated Transfer Learning for On-Device LLMs Efficient Fine Tuning... | 19 | 101 | 2 |


### Tabel C. Ringkasan kluster bibliographic coupling (kluster ≥6 dokumen)

| Kluster (warna) | Label kluster | Jumlah publikasi | Blok asal | Publikasi representatif |
|---|---|---|---|---|
| 1 (merah) | [BELUM DIBERI NAMA] | 28 | {'B': 26, 'A': 2} | Wang et al. (2025), Empowering large language models to edge intelligence: A survey of edge...; Sun et al. (2024), A review of AI edge devices and lightweight CNN and LLM deployment |
| 2 (hijau) | [BELUM DIBERI NAMA] | 25 | {'B': 25} | Shao et al. (2025), Imp: Highly Capable Large Multimodal Models for Mobile Devices; Zhang et al. (2024), EdgeTA: Neuron-Grained Scaling of Foundation Models in Edge-Side Retraining |
| 3 (biru) | [BELUM DIBERI NAMA] | 25 | {'B': 21, 'C': 2, 'A': 1, 'A+C': 1} | Friha et al. (2024), LLM-Based Edge Intelligence: A Comprehensive Survey on Architectures,...; Piccialli et al. (2024), Federated and edge learning for large language models |
| 4 (kuning) | [BELUM DIBERI NAMA] | 22 | {'B': 22} | Wang et al. (2025), Split Learning Based Cloud-Edge-End Collaborative Model Training in...; Semerikov et al. (2025), Edge intelligence unleashed: a survey on deploying large language models in... |


## Co-citation

Dari 10422 referensi unik, 530 memenuhi ambang 3 sitasi oleh dokumen kita (setelah 10 artefak dibuang), membentuk 5 kluster (ukuran: [175, 147, 96, 72, 40]).

### Tabel D. Top 10 dokumen dengan co-citation dan TLS tertinggi

| Peringkat | Dokumen | Sitasi (oleh dokumen kita) | TLS | Kluster |
|---|---|---|---|---|
| 1 | Brown (2020), Language Models are Few-Shot Learners | 28 | 582 | 4 |
| 2 | Touvron (2023), LLaMA: Open and Efficient Foundation Language Models | 17 | 529 | 4 |
| 3 | Vaswani (2017), Attention Is All You Need | 27 | 521 | 2 |
| 4 | Kwon (2023), Efficient Memory Management for Large Language Model Serving with PagedAttention | 25 | 508 | 2 |
| 5 | Ma (2023), LLM-Pruner: On the Structural Pruning of Large Language Models | 19 | 507 | 2 |
| 6 | Shen (2024), Agile-Quant: Activation-Guided Quantization for Faster Inference of LLMs on the... | 10 | 449 | 3 |
| 7 | Dettmers (2023), QLoRA: Efficient Finetuning of Quantized LLMs | 26 | 437 | 2 |
| 8 | Liu (2024), LLM-QAT: Data-Free Quantization Aware Training for Large Language Models | 11 | 411 | 2 |
| 9 | Yi (2025), EdgeMoE: Empowering Sparse Large Language Models on Mobile Devices | 13 | 398 | 3 |
| 10 | Ainslie (2023), GQA: Training Generalized Multi-Query Transformer Models from Multi-Head... | 12 | 392 | 2 |


### Tabel E. Kluster co-citation

| Kluster (warna) | Label kluster | Jumlah artikel | Publikasi representatif |
|---|---|---|---|
| 1 (merah) | [BELUM DIBERI NAMA] | 175 | Zhang (2024), EdgeShard: Efficient LLM Inference via Collaborative Edge Computing; Zheng (2025), A Review on Edge Large Language Models: Design, Execution, and Applications |
| 2 (hijau) | [BELUM DIBERI NAMA] | 147 | Vaswani (2017), Attention Is All You Need; Dettmers (2023), QLoRA: Efficient Finetuning of Quantized LLMs |
| 3 (biru) | [BELUM DIBERI NAMA] | 96 | Wei (2022), Chain-Of-Thought Prompting Elicits Reasoning in Large Language Models; Shi (2016), Edge Computing: Vision and Challenges |
| 4 (kuning) | [BELUM DIBERI NAMA] | 72 | Brown (2020), Language Models are Few-Shot Learners; Touvron (2023), LLaMA: Open and Efficient Foundation Language Models |
| 5 (ungu) | [BELUM DIBERI NAMA] | 40 | Ding (2023), Parameter-efficient fine-tuning of large-scale pre-trained language models; Wolf (2020), Transformers: State-of-the-Art Natural Language Processing |


## Co-word

Dari 3043 kata kunci unik (setelah penggabungan sinonim dan membuang 'large language model' serta 'artificial intelligence'), 100 memenuhi ambang 8 kemunculan, membentuk 3 kluster (ukuran: [48, 39, 13]).

### Tabel F. Top 15 kata kunci dalam analisis co-occurrence

| Peringkat | Kata kunci | Kemunculan | TLS | Kluster |
|---|---|---|---|---|
| 1 | edge computing | 109 | 346 | 1 |
| 2 | retrieval-augmented generation | 78 | 194 | 2 |
| 3 | edge deployment | 64 | 205 | 1 |
| 4 | on-device inference | 63 | 177 | 1 |
| 5 | model compression | 61 | 267 | 1 |
| 6 | small language models | 59 | 187 | 1 |
| 7 | resource-constrained devices | 52 | 214 | 1 |
| 8 | energy efficiency | 50 | 166 | 1 |
| 9 | local large language models | 48 | 79 | 2 |
| 10 | multi-agent systems | 44 | 106 | 2 |
| 11 | edge devices | 42 | 108 | 3 |
| 12 | generative ai | 42 | 138 | 2 |
| 13 | data privacy | 40 | 117 | 2 |
| 14 | federated learning | 37 | 139 | 3 |
| 15 | agentic ai | 36 | 98 | 2 |


### Tabel G. Ringkasan analisis co-word

| Kluster (warna) | Label kluster | Jumlah kata kunci | Kata kunci representatif |
|---|---|---|---|
| 1 (merah) | [BELUM DIBERI NAMA] | 48 | edge computing, edge deployment, on-device inference, model compression, small language models, resource-constrained devices, energy efficiency, knowledge distillation |
| 2 (hijau) | [BELUM DIBERI NAMA] | 39 | retrieval-augmented generation, local large language models, multi-agent systems, generative ai, data privacy, agentic ai, llm agents, inventory management |
| 3 (biru) | [BELUM DIBERI NAMA] | 13 | edge devices, federated learning, low-rank adaptation, parameter-efficient fine-tuning, privacy preservation, multimodal large language models, differential privacy, communication efficiency |


Catatan: warna kluster mengikuti urutan standar VOSviewer (1 merah, 2 hijau, 3 biru, 4 kuning, 5 ungu); cocokkan dengan gambar yang kamu ekspor.
