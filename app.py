import streamlit as st
import streamlit.components.v1 as comps
from langchain import PromptTemplate, HuggingFaceHub, LLMChain
import requests
import os

def main():
    st.title('Website Preview')
    user_text = st.text_input("Enter text:", "")
    
    if user_text:
        st.write("You entered:", user_text)

        # Define the prompt template
        prompt = PromptTemplate(
            input_variables=["text"],
            template='''Task: {text}

            Objective:
            Design and implement a product website showcasing a fictional product using HTML, CSS, and JavaScript in a single file. The website should have the following sections:

            Header Section: Create a header section with a navigation menu and any relevant branding elements.
            Hero Section: Design a hero section that prominently displays the product with a compelling headline and call-to-action button.
            Features Section: Develop a section that highlights key features of the product using vibrant colors and fonts.
            Pricing Section: Implement a pricing section that displays different pricing plans or options for the product.
            Banner: Incorporate a banner section to grab attention and convey important messages or promotions.
            FAQ Section: Include a frequently asked questions (FAQ) section where users can find answers to common queries about the product.
            Footer: Create a footer section with links to important pages, social media icons, and any other relevant information.
            
            Instructions:

            HTML Structure:
            Use semantic HTML elements for better accessibility and SEO.
            Structure the page with appropriate sections and divs for each component.

            CSS Styling:
            Apply inline CSS to style each section.
            Use vibrant colors and modern fonts to enhance visual appeal.
            Ensure responsive design to optimize for various screen sizes.

            JavaScript Interactivity:
            Use JavaScript to add interactivity to the website, such as smooth scrolling, form validation, or interactive elements.

            Third-Party Libraries/Frameworks:
            Utilize open-source third-party libraries or frameworks to enhance creativity and functionality if desired. Examples include Bootstrap, jQuery, or Font Awesome.

            Modern Coding Techniques:
            Implement modern coding techniques, such as flexbox or grid layout for responsiveness and CSS variables for easier customization.
            Optimize code for performance and efficiency to ensure fast loading times.

            Deliverables:
            Submit a single HTML file containing the complete code for the product website including CSS and JavaScript. The website should be visually appealing, user-friendly, and fully functional.'''
        )

        chain=LLMChain(llm=HuggingFaceHub(repo_id='mistralai/Mistral-7B-Instruct-v0.2', model_kwargs={'temperature':0.1, 'max_new_tokens':8000}, huggingfacehub_api_token="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"), prompt=prompt)
        code=chain.invoke(user_text)

        doctype_index = code['text'].find("<!DOCTYPE html>")
        doctype_index_last=code['text'].find("</html>")
        final_code=code['text'][doctype_index:doctype_index_last+7]

        file_path = os.path.join("public", "index.html")
        with open(file_path, "w") as file:
            file.write(final_code)


        # URL for website preview
        website_url = "https://theuselessweb.com/"
        
        comps.iframe(website_url, height=500, scrolling=True)
        st.text(f'Hosted Link: {website_url}')

if __name__ == "__main__":
    main()
