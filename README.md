# 🌙 王秋月 · AI智能助手

> 基于 DeepSeek 大模型的多功能 AI Agent | 张羽 独立开发

[![Gitee](https://img.shields.io/badge/Gitee-仓库-red)](https://gitee.com/zhangyu202/agent-study)
[![GitHub](https://img.shields.io/badge/GitHub-仓库-black)](https://github.com/yuzhangdev/wangqiuyue-agent)

---

## 🧠 核心功能

| 功能 | 说明 | 状态 |
|------|------|:--:|
| 💬 多轮对话 | 上下文记忆，连续聊天 | ✅ |
| 🧠 向量记忆 | FAISS 语义搜索，长期记忆 | ✅ |
| 🔧 工具调用 | 时间/计算/笑话/天气/新闻 | ✅ |
| 📊 Excel分析 | 上传即分析，自动出图 | ✅ |
| 📚 RAG文档问答 | 上传文档，基于内容回答 | ✅ |
| 📋 自主规划 | 任务拆解→逐步执行→总结 | ✅ |
| 🌐 联网搜索 | Bing搜索+AI总结 | ✅ |
| 📧 邮件发送 | AI写邮件+自动发送 | ✅ |
| 🎤 语音播报 | 文字转语音 | ✅ |
| 👥 多Agent协作 | 研究员→写手→审核→总结 | ✅ |

---

## 🛠️ 技术栈

- **大模型**: DeepSeek API (deepseek-chat)
- **框架**: LangChain, Streamlit
- **数据库**: FAISS (向量记忆), JSON
- **数据处理**: Pandas, Matplotlib, OpenPyXL
- **其他**: Whisper (语音识别), SMTP (邮件)

---

## 🚀 快速启动

```bash
# 安装依赖
pip install streamlit pandas matplotlib openpyxl requests python-dotenv langchain langchain-openai faiss-cpu

# 设置API Key（在.env文件中）
DEEPSEEK_API_KEY=sk-your-key

# 启动终极版
streamlit run projects/wangqiuyue_ultimate.py