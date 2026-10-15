import speech_recognition as sr


recognizer = sr.Recognizer()

recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 1.5
recognizer.phrase_threshold = 0.3
recognizer.non_speaking_duration = 0.8


# ==========================================
# NORMALIZE SPEECH
# ==========================================

def normalize_speech(text):

    text = text.strip()

    replacements = {
        "n y x": "nyx",
        "n, y, x": "nyx",
        "n-y-x": "nyx",
        "N Y X": "NYX",
        "N, Y, X": "NYX",
        "N-Y-X": "NYX",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text


# ==========================================
# LISTEN
# ==========================================

def listen():

    try:

        with sr.Microphone() as source:

            print("\n🎤 NYX is listening...")

            audio = recognizer.listen(
                source,
                timeout=10,
                phrase_time_limit=60
            )

        print("🧠 Processing complete command...")

        command = recognizer.recognize_google(audio)

        command = normalize_speech(command)

        print(f"📝 Recognized: {command}")

        return command

    except sr.WaitTimeoutError:

        print("⏱️ No speech detected.")
        return ""

    except sr.UnknownValueError:

        print("❌ NYX could not understand.")
        return ""

    except sr.RequestError as e:

        print(f"❌ Speech recognition error: {e}")
        return ""