# Python DApp Template

First It needs to download model files from https://huggingface.co/mys/ggml_llava-v1.5-7b/tree/main . Here you need to download ggml-model-q4_k.gguf and mmproj-model-f16.gguf then put into dapp_llava folder without changing names(if its put into different location code and dockerfile needs to be updated)

Cmake is compiled for RISC-V architecture and in order to save time We added releated files which can be copied into docker image