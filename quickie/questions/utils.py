def serialize_question(question):
    return {
        "id": question.id,
        "question": question.question,
        "answer": question.answer,
        "difficulty": question.difficulty,
        "category_id": question.category_id,
    }
