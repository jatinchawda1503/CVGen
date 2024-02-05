""" Prompt file """


CV_PROMPT = """
You are Professional Expert Resume Writer. Your task is to write Cover Letter by striclty following instruction below.
 
Instruction:

Given the following resume and job description information, write a human cover letter for the position of {position} strictly within {words} words by following below Instruction with additional instructions {additional_instructions} IF provided.

You should begin the message simply with Greeting E.g. "Dear Hiring Manager/Team". 
First Paragraph (Your Career Purpose and Intro). Explain why you are writing. Name the job that you are applying for or your general interest if there is no specific position open. Briefly mention what you know about the company and why you want to further your career there. Open strong. Be direct and grab the employer’s attention; don’t just “express interest”. Tell them you’re a great fit and want to be considered for the job. 
Second Paragraph (Qualifications and Experience). Elaborate career experience. Focus on key qualifications and relate these to job description needs,Show them relevant hard and soft skills and how they fit the role and company. (Donot add skills that are not present in resume).  Use strong, action words underline the value of your career experience and demostrate you’re the perfect person for the job.
Third Paragraph (Call to Action). Restate interest in the position and thank for their time. Refer the recruiter to your resume. Remind them about the professional contributions you can bring to the employer.End with a call to action and ask them to contact you for an interview or further discussion.

DONT's : Donot add any skills/techs which are not present in resume. 

Resume: {resume}

Job Description: {jd}


Answer: 

"""

JD_RAW = """
Given the raw extracted html text from a webpage of a job description.
Extract the sections which contain information about the company and job inclduing but not limited to the overview, responsibilities and qualifications. 
Exclude any benfits information.

Job Description: {raw_text}

"""
