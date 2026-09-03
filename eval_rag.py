from embedding_search import semantic_document_search


TEST_CASES = [
    {
        "question": "What allowance helps with relocation-related expenses?",
        "expected_sources": [
            "s1_reference.txt",
            "MCO 5000.14D.pdf"
        ]
    },
    {
        "question": "What system manages Marine Corps total force information?",
        "expected_sources": [
            "s1_reference.txt",
            "MCO 5000.14D.pdf"
        ]
    },
    {
        "question": "What should a unit check before escalating an administrative issue?",
        "expected_sources": [
            "training_reference.txt"
        ]
    },
    {
        "question": "Tell me about personnel administration.",
        "expected_sources": [
            "training_reference.txt",
            "MCO 5000.14D.pdf"
        ]
    }
]


def run_evaluation():
    passed = 0

    print("RAG RETRIEVAL EVALUATION")
    print("========================")

    for number, test_case in enumerate(TEST_CASES, start=1):
        question = test_case["question"]
        expected_sources = test_case["expected_sources"]

        results = semantic_document_search(
            question,
            top_k=3
        )

        retrieved_sources = [
            result["document_name"]
            for result in results
        ]

        success = any(
            source in retrieved_sources
            for source in expected_sources
        )

        if success:
            passed += 1
            status = "PASS"
        else:
            status = "FAIL"

        print(f"\nTest {number}: {status}")
        print(f"Question: {question}")
        print(
            f"Acceptable sources: "
            f"{expected_sources}"
        )
        print(
            f"Retrieved sources: "
            f"{retrieved_sources}"
        )

    total = len(TEST_CASES)
    accuracy = passed / total

    print("\n========================")
    print(f"Passed: {passed}/{total}")
    print(
        f"Retrieval accuracy: "
        f"{accuracy:.0%}"
    )


if __name__ == "__main__":
    run_evaluation()