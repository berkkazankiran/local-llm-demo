@echo off
curl.exe http://127.0.0.1:11434/api/chat -H "Content-Type: application/json" -d "{\"model\":\"llama3.2:3b\",\"messages\":[{\"role\":\"user\",\"content\":\"What is the capital of Turkey? Answer in one sentence.\"}],\"stream\":false}"
