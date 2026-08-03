import speech_recognition as sr
r = sr.Recognizer()
with sr.Microphone() as source:
    print("🎙️ 开始听，请说话...")
    r.adjust_for_ambient_noise(source, duration=1)
    try:
        audio = r.listen(source, timeout=3)
        print("✅ 听到了！正在识别...")
        text = r.recognize_google(audio, language='zh-CN')
        print(f"👤 你说的是：{text}")
    except sr.WaitTimeoutError:
        print("⏰ 超时，没听到声音")
    except Exception as e:
        print(f"❌ 错误：{e}")