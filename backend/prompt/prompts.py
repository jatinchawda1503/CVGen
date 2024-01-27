CV_PROMPT = """

Instruction:
You are Professional Expert Writer. 
Given the following resume and job description information, write a human cover letter for the position of {position}  within {words} by following below Instruction with additional instructions {additional_instructions} IF provided.

You should begin the message simply with Greeting "Dear Hiring Manager/Team". 
First Paragraph (Your Career Purpose and Intro). Explain why you are writing. Name the job that you are applying for or your general interest if there is no specific position open. Briefly mention what you know about the company and why you want to further your career there. Open strong. Be direct and grab the employer’s attention; don’t just “express interest”. Tell them you’re a great fit and want to be considered for the job. 
Second Paragraph (Qualifications and Experience). Elaborate career experience. Focus on key qualifications and relate these to job description needs,Show them relevant hard and soft skills and how they fit the role and company. (Donot add skills that are not present in resume).  Use strong, action words underline the value of your career experience and demostrate you’re the perfect person for the job.
Third Paragraph (Call to Action). Restate interest in the position and thank for their time. Refer the recruiter to your resume. Remind them about the professional contributions you can bring to the employer.End with a call to action and ask them to contact you for an interview or further discussion.


Resume: {resume}

Job Description: {jd}

Answer:

"""

JD_RAW = """
Given the text from a webpage of a job description.
Extract the sections which contain information about the company and job inclduing but not limited to the overview, responsibilities and qualifications. 
Exclude any benfits information.

Job Description: {raw_text}

"""

CV_PROMPT_2 = """

Instruction:
You are Expert Writer. 
Given the following resume and job description information, write a human cover letter for the position of {position}  within {words} by following below Instruction.. 
You should begin the message simply with "Hi, I'm <my name>, <a short tagline created for me>" and follow it up with one short information dense paragraph using business causal language. 
You should highlight any overlap of technology, responsibility or domain present between the job listing and my experience while mentioning why I would be a good fit for the given role. 
You should use optimistic and affirmative language and end the message with a call to action. Be concise.

Job Description: {jd}

Resume: {resume}

Answer:

"""