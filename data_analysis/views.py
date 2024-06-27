# data_analysis/views.py
import pandas as pd
from django.conf import settings
from django.shortcuts import render
from groq import Groq

from .forms import DataForm


def analyze_data(request):
    if request.method == 'POST':
        form = DataForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            question = form.cleaned_data['question']

            # Baca file Excel ke DataFrame
            df = pd.read_excel(file)

            # Konversi DataFrame ke teks
            data_text = df.to_csv(index=False)

            # Buat prompt untuk API Groq AI
            prompt = f"Data:\n{data_text}\n\nPertanyaan: {question}\n\nBerikan saya jawabannya saja dengan singkat dan berbahasa indonesia."

            # Gunakan library Groq untuk membuat permintaan
            client = Groq(api_key=settings.GROQ_API_KEY)

            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "Anda adalah seorang asisten yang membantu dalam analisis data."
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="llama3-70b-8192",
                temperature=0.5,
                max_tokens=1024,
                top_p=1,
                stop=None,
                stream=False,
            )

            # Proses respons dari API Groq AI
            ai_response = chat_completion.choices[0].message.content

            return render(request, 'result.html', {'response': ai_response})

    else:
        form = DataForm()

    return render(request, 'upload.html', {'form': form})
