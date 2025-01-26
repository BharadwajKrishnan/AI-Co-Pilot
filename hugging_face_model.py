from huggingface_hub import InferenceClient

class HuggingFace_Matrickz():
    def __init__(self):
        self.api_key = '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'

        # Provide the access token
        self.client = InferenceClient(api_key=self.api_key)

        # Initialize the message history with the system's context message
        self.message_history = [
            {
                "role": "system",
                "content": "I want you to be an automotive system's enginnering expert. I want you to be able to write system requirements for any automotive system."
                           "I want you to ask me questions and take technical inputs from me about the system. You must not assume any technical functionality."
                           "Always ask me questions one by one."
            }
        ]

    def query(self, text, file_content):
        # Append file content to message history if provided
        if file_content:
            self.message_history.append({
                "role": "user",
                "content": file_content
            })

        # Add the current user input to the message history
        self.message_history.append({
            "role": "user",
            "content": text
        })

        # Call the LLM API with the updated message history
        completion = self.client.chat.completions.create(
            model="meta-llama/Meta-Llama-3-8B-Instruct",
            messages=self.message_history,
            max_tokens=500
        )

        # Get the assistant's response
        assistant_response = completion.choices[0].message.content

        # Append the assistant's response to the message history
        self.message_history.append({
            "role": "assistant",
            "content": assistant_response
        })

        return assistant_response

