# 🧠 Eve - A Modular AI Assistant Powered by LLaMA 3

**Eve** is a JSON-aware AI assistant built using the LLaMA 3 (3B) model and a powerful modular tool-calling architecture. It intelligently determines when to invoke external tools like weather APIs, Google search, or news services based on user queries — and responds naturally with the help of response prompts.

---

## 🚀 Features

- 🔄 **Modular Tool Execution**: Eve can dynamically call the appropriate tool (weather, news, search) by analyzing natural language.
- 🧠 **System Prompt Design**: Separates thinking and responding with dedicated system prompts for tool detection and natural reply.
- 📡 **Streaming LLM Output**: Uses streaming response for a more interactive feel.
- 🔧 **Custom Tool Integration**: Add your own tools by registering them in the `TOOLS` dictionary.
- 💬 **Natural Language Output**: LLaMA model generates human-like responses based on real-time tool data.

---

## 🛠️ Installation

```bash
git clone https://github.com/Piyush2102020/eve.git
cd eve
pip install -r requirements.txt
