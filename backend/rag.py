from ai_service import ask_ai


def answer_question(question, chunks):
    context = "\n\n".join(chunks)

    return ask_ai(
        question=question,
        context=context
    )
