import streamlit as st
from langchain_anthropic import ChatAnthropic
import base64
import os

# Set page config for a modern look
st.set_page_config(
    page_title="Pallavi's Job Application Wizard ✨",
    page_icon="🎨",
    layout="centered"
)

# Custom CSS for a more modern look
st.markdown("""
    <style>
    .stButton>button {
        background-color: #FF4B4B;
        color: white;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #FF6B6B;
        border-color: #FF6B6B;
    }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

os.environ["ANTHROPIC_API_KEY"] = st.secrets["ANTHROPIC_API_KEY"]

# Your resume text (keeping this unchanged)
RESUME = """PALLAVI JAIN
157 West 106th St, 10025, New York, NY
(413)-321-4265 | pj2421@columbia.edu | www.linkedin.com/in/pallavijain2198
EDUCATION
Columbia University New York, NY
Masters in Advanced Architectural Design Savitribai Phule Pune University May 2024
Pune, India
Bachelor of Architecture Aug 2021
SKILLS
Digital Representation: AutoCAD, SketchUp, V-Ray, Rhinoceros 3D, Revit, TwinMotion, Blender, Enscape, Lumion, Adobe Photoshop, Adobe
Illustrator, Adobe InDesign, Microsoft Office Suite
Physical Representation: 3D Printing, Document Research, Model Making, Wood-Cutting, Laser Cutting
WORK EXPERIENCE
Columbia University (GSAPP) Associate Faculty New York, NY
Aug 2024 – present
▪ Assisting an Advanced Architectural Design Studio exploring zero-carbon, climate-adaptive strategies for Paris by 2100. Guiding
students through research on climate phenomena.
▪ Mentoring students in designing sustainable, climate-resilient urban spaces, focusing on innovative solutions for heatwaves, droughts,
and flooding in a warming world, inspired by vernacular architecture and environmental principles.
Columbia University (GSAPP) Teaching Assistant: Tech V - Construction and Life Cycle Systems New York, NY
Jan 2024 – May 2024
▪ Delivered advanced content on construction systems, life cycle analysis, and sustainable design, mentoring students in practical
applications, including 3D life cycle assessments and 1:1 fabrication work.
▪ Enhanced students' grasp of sustainable methodologies through hands-on guidance, leading to a deeper practical application in their
studio projects.
P-Cube Design Studio Satna, India
Architect May 2022 – May 2024
▪ Pioneered a kinetic façade design for an 4-story apartment building in India, enhancing thermal efficiency through advanced materials
and engineering techniques, supporting sustainable building practices.
▪ Led multidisciplinary teams on large-scale projects, including an 8-acre gated residential community and a 3-acre resort, delivering
innovative design solutions from concept to completion.
Sheetal Kumar & Associates Junior Architect Jaipur, India
April 2021 – Mar 2022
▪ Directed the design of a luxurious 8-bedroom villa, creating CAD drawings and 3D models while crafting detailed working drawings
for bespoke furniture to elevate both aesthetics and functionality.
▪ Led cost estimations and Bill of Quantities (BOQs) for residential row housing, designing floor plans that blend functionality with
contemporary living standards.
Kothari & Associates Raipur, India
Architectural Intern Aug 2020 – Dec 2020
▪ Crafted ergonomic designs for office and residential projects, including a bespoke bungalow for a state senator, enhancing both
function and client satisfaction.
▪ Specialized in creating detailed 3D visualizations and presentations, showcasing design concepts for client approval, emphasizing
tailored solutions and aesthetic excellence.
RESEARCH
Refurbishing Techniques for Substantiality in Architecture
▪ Investigated innovative refurbishment methods to enhance building sustainability focusing on extending the lifecycle of materials and
structures, reducing environmental impact, and promoting energy efficiency.
Terracotta Screens for Passive Cooling
▪ Delved into the use of terracotta screens for sustainable passive cooling in buildings highlighting the potential of traditional materials
and techniques, showcasing terracotta's effectiveness in reducing energy consumption and enhancing thermal comfort.
CERTIFICATIONS
▪ Introduction to LEEDS v4.1 for Design and Construction | U.S. Green Building Council
▪ Introduction to LEEDS v4.1 for existing buildings | U.S. Green Building Council
▪ Transportation, Sustainable Buildings and Green Construction | John Hopkins University
▪ The Language of Design: Form and Meaning | California Institute of the Arts"""


# System template (keeping this unchanged)
SYSTEM_TEMPLATE = f"""
You are an expert career consultant and professional writer specializing in architectural and design positions. Your task is to create:
1. A compelling, tailored cover letter
2. A concise, engaging application email

Use the following resume information:
{RESUME}

For the cover letter:
- Start with a powerful hook showing understanding of the role and company
- Match your experiences directly to their specific needs
- Demonstrate impact using metrics and specific achievements
- Show how your unique combination of skills adds value
- Emphasize sustainable design experience and innovative solutions
- Showcase project management and technical expertise
- Use active voice and industry-specific terminology naturally
- End with enthusiasm and a clear call to action

For the application email:
- Create an attention-grabbing subject line
- Keep the body brief but compelling
- Mention attached documents
- End with a strong call to action

Remember to:
- Customize content to directly address the job requirements
- Use specific examples that best match the position
- Show enthusiasm for the role and company
- Demonstrate how your background makes you an ideal candidate

Separate the cover letter and email with "---EMAIL---" on its own line.
The email should start with "Subject: [Your suggested subject line]"
"""


def init_claude():
    return ChatAnthropic(
        model="claude-3-5-sonnet-20241022",
    )

def main():
    # Header with emoji and welcome message
    st.title("✨ Pallavi's Job Application Wizard")
    st.markdown("""
        ### 🎨 Turn Job Descriptions into Cover Letters and Emails!
        Hello madam! Let's help you craft the perfect job application materials for your next architectural adventure! 
        Just paste the job description below, and done ! 
    """)
    
    try:
        st.session_state.claude = init_claude()
    except Exception as e:
        st.error(f"Oops! Something went wrong while initializing: {str(e)} 😅")
        return

    # Job description input with a more friendly prompt
    st.subheader("🎯 What's the target Job?")
    job_description = st.text_area(
        "Paste the job description here:",
        height=200,
        placeholder="Paste the complete job description here. The more details, the better! 🚀"
    )
    
    # Additional info with expandable section
    with st.expander("🌟 Want to add more context?"):
        additional_info = st.text_area(
            "Additional Information (Optional):",
            height=100,
            placeholder="More about the company culture, specific projects, or anything else that might be relevant! 💫"
        )

    # Fun loading message options
    loading_messages = [
        "🎨 Crafting your perfect application...",
        "✍️ Adding that special touch...",
        "🌟 Making your application shine...",
        "🏗️ Building something amazing...",
        "🎭 Getting creative..."
    ]

    if st.button("✨ Generate My Application Materials!", use_container_width=True):
        if not job_description:
            st.error("Oops! We need a job description to work our magic! 🎭")
            return

        try:
            with st.spinner(choice(loading_messages)):
                # Create and format prompt
                user_prompt = f"""
                Job Description: {job_description}
                Additional Information: {additional_info if additional_info else 'Not provided'}

                Please generate a tailored cover letter and application email for this position.
                """
                
                messages = [
                    {"role": "system", "content": SYSTEM_TEMPLATE},
                    {"role": "user", "content": user_prompt}
                ]

                # Generate content
                response = st.session_state.claude.invoke(messages).content

                # Split response into cover letter and email
                cover_letter, email = response.split("---EMAIL---")

                # Display results in nice containers
                st.success("🎉 Your application materials are ready!")
                
                with st.container():
                    st.subheader("📝 Cover Letter")
                    st.markdown(cover_letter.strip())
                    st.download_button(
                        label="📥 Download Cover Letter",
                        data=cover_letter.strip(),
                        file_name="cover_letter.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                
                st.divider()
                
                with st.container():
                    st.subheader("📧 Application Email")
                    st.markdown(email.strip())
                    st.download_button(
                        label="📥 Download Email",
                        data=email.strip(),
                        file_name="application_email.txt",
                        mime="text/plain",
                        use_container_width=True
                    )

        except Exception as e:
            st.error(f"Oops! Something went wrong: {str(e)} 🎭")

if __name__ == "__main__":
    from random import choice
    main()