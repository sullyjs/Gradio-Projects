import openai #importing OpenAI API to use their language model
import gradio #importing Gradio library for creating a web interface for this model
import re #importing regular expression module to find mentions of race and sex

#setting OpenAI API key
openai.api_key = "API key"

#defining a function that takes in various inputs related to a medical case and uses GPT-3.5 language model to generate a response
def CustomChatGPT(Race, Sex, Residency, GymRequest):
    #creating a new messages list for this interaction, with a prompt for the model to respond to
    messages = [{"role": "system", "content": "You are an in-person gym instructor who specializes in strength training. You have been working in a gym called Basic Fit and members come in, to whom you suggest a certain workout training, referencing amount of sets, reps and different exercises they could practice. You give these recommendations, basing on which muscles they want to train. You base these recommendations on who the patient is, what they tell you they want to train, what their body looks like, what sex they are, what race they are, and the available physical body and strength exercise studies that make assumptions and conclusions based on these factors. Your answers exist of what exercises they should do, how many sets and reps, and what goals they will achieve doing this.”"}]
    #creating a prompt for the model based on the inputs
    Case= f"Act as a gym instructor. I am a {Race} {Sex} gym enthusiast with the following residency situation: {Residency}. I have the following request: {GymRequest}. What is the best workouts I could do?"
    messages.append({"role": "user", "content": Case})
    #using OpenAI API to generate a response to the prompt
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = messages)
    #extracting the response from the API's output
    ChatGPT_reply = response["choices"][0]["message"]["content"]
    #adding the model's response to the messages list
    messages.append({"role": "assistant", "content": ChatGPT_reply})
    #calculating the number of words and paragraphs in the model's response
    word_count = len(ChatGPT_reply.split())
    paragraph_count = ChatGPT_reply.count("\n\n") + 1
    #returning the model's response along with the word, paragraph, race and gender count
    
    #writing input and output information to the file
    with open("neuromed_capstone_data.txt", "a") as file:
        file.write("Input:\n")
        file.write(f"Race: {Race}\n")
        file.write(f"Sex: {Sex}\n")
        file.write(f"Residency: {Residency}\n")
        file.write(f"Health Issue: {GymRequest}\n\n")
        
        file.write("Output:\n")
        file.write(f"ChatGPT Response: {ChatGPT_reply}\n")
        file.write(f"Word count: {word_count} words\n")
        file.write(f"Paragraph count: {paragraph_count} paragraphs\n")
        file.write("-------------------------------------\n")
    
    return ChatGPT_reply, str(word_count) + " words", str(paragraph_count) + " paragraphs"


#creating a Gradio interface for the model's function with appropriate inputs and outputs
demo = gradio.Interface(fn=CustomChatGPT, inputs=["text", "text", "text", "text"], 
                        outputs=[gradio.outputs.Textbox(label="ChatGPT Response"), gradio.outputs.Textbox(label="Word count"),
                                gradio.outputs.Textbox(label="Paragraph count")],
                        title="Gym Instructor", 
                        theme=gradio.themes.Soft(primary_hue="blue").set(loader_color="#89CFF0"))

#launching the Gradio interface
demo.launch(share=False)
