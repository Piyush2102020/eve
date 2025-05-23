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
git clone https://github.com/your-username/eve-ai-assistant.git
cd eve-ai-assistant
pip install -r requirements.txt
````

---

## 🔑 API Keys

Set the following environment variables before running:

| API               | Variable Name                      | Where to Get It                                                                     |
| ----------------- | ---------------------------------- | ----------------------------------------------------------------------------------- |
| Weather API       | `WEATHER_API_KEY`                  | [weatherapi.com](https://www.weatherapi.com/)                                       |
| News API          | `NEWS_API_KEY`                     | [newsapi.org](https://newsapi.org/)                                                 |
| Google Search API | `SEARCH_API_KEY` + `SEARCH_CSX_ID` | [programmablesearchengine.google.com](https://programmablesearchengine.google.com/) |

You can use a `.env` file and load it via [`python-dotenv`](https://pypi.org/project/python-dotenv/).

---

## 🧬 Architecture

* `SYSTEM_PROMPT_TOOL`: Decides **which tool to call** (e.g., weather, search) based on input.
* `SYSTEM_PROMPT_RESPONDER`: Uses tool response + user query to generate a natural reply.
* `Eve.run()`: Main loop for user interaction.
* Tool modules: Defined in separate files (e.g., `weather.py`, `news.py`, `google.py`).

---

## ▶️ Running Eve

```bash
python eve.py
```

Start chatting with Eve via terminal. Use `break` to exit.

## 📄 License

MIT License — open-source and free to use.

---

## ✨ Credits

Built with ❤️ by [Piyush Bhatt](https://github.com/Piyush2102020).
Model: [LLaMA 3 3B](https://ai.meta.com/llama/).
Assistant Identity: Eve.

