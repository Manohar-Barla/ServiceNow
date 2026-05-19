import re
import io
from .models import Question

def extract_text_from_file(file_obj, filename):
    ext = filename.split('.')[-1].lower()
    text = ""
    
    if ext == 'txt':
        text = file_obj.read().decode('utf-8', errors='ignore')
    elif ext == 'pdf':
        import pdfplumber
        with pdfplumber.open(file_obj) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    elif ext == 'docx':
        from docx import Document
        doc = Document(file_obj)
        for para in doc.paragraphs:
            text += para.text + "\n"
            
    return text

def parse_questions_file(file_obj, filename):
    text = extract_text_from_file(file_obj, filename)
    if not text:
        return 0, "Could not extract text from the file."

    # Split into blocks based on "Question No:"
    blocks = re.split(r'(?i)^Question\s*No:\s*', text, flags=re.MULTILINE)
    
    saved_count = 0
    errors = []
    
    for i, block in enumerate(blocks):
        if not block.strip():
            continue
            
        try:
            # Re-attach the splitting text part essentially by assuming it starts with the number
            block_lines = [line.strip() for line in block.strip().split('\n') if line.strip()]
            
            # The first line should be the number
            q_num_str = block_lines[0].split()[0]
            question_number = int(re.sub(r'\D', '', q_num_str)) if re.sub(r'\D', '', q_num_str) else None
            
            # Extract Question Type
            q_type_match = re.search(r'(?i)Question\s*Type:\s*(.+)', block)
            question_type = q_type_match.group(1).strip().upper() if q_type_match else "SINGLE_CHOICE"
            if question_type not in ['SINGLE_CHOICE', 'MULTIPLE_SELECT']:
                question_type = 'SINGLE_CHOICE'
                
            # Extract Topic
            topic_match = re.search(r'(?i)Topic:\s*(.+)', block)
            topic = topic_match.group(1).strip() if topic_match else "Platform"
            
            # Extract Question
            q_text_match = re.search(r'(?i)Question:\s*(.+?)(?=\nOptions:)', block, re.DOTALL)
            question_text = q_text_match.group(1).strip() if q_text_match else ""
            
            # Extract Options
            options_match = re.search(r'(?i)Options:\s*(.+?)(?=\nCorrect\s*Answers?:)', block, re.DOTALL)
            options_text = options_match.group(1).strip() if options_match else ""
            
            option_a = option_b = option_c = option_d = option_e = ""
            for opt_line in options_text.split('\n'):
                opt_line = opt_line.strip()
                if opt_line.upper().startswith('A.'): option_a = opt_line[2:].strip()
                elif opt_line.upper().startswith('B.'): option_b = opt_line[2:].strip()
                elif opt_line.upper().startswith('C.'): option_c = opt_line[2:].strip()
                elif opt_line.upper().startswith('D.'): option_d = opt_line[2:].strip()
                elif opt_line.upper().startswith('E.'): option_e = opt_line[2:].strip()

            # Extract Correct Answers
            ans_match = re.search(r'(?i)Correct\s*Answers?:\s*(.+)', block)
            correct_answers = ans_match.group(1).strip() if ans_match else ""
            
            # Extract Explanation if any
            exp_match = re.search(r'(?i)Explanation:\s*(.+)', block, re.DOTALL)
            explanation = exp_match.group(1).strip() if exp_match else ""

            if question_text and option_a and option_b and correct_answers:
                Question.objects.create(
                    question_number=question_number,
                    question_type=question_type,
                    topic=topic,
                    question_text=question_text,
                    option_a=option_a,
                    option_b=option_b,
                    option_c=option_c,
                    option_d=option_d,
                    option_e=option_e,
                    correct_answers=correct_answers,
                    explanation=explanation
                )
                saved_count += 1
            else:
                errors.append(f"Block {i} missing required fields.")
        except Exception as e:
            errors.append(f"Error parsing block {i}: {str(e)}")

    if errors:
        return saved_count, "\n".join(errors)
    return saved_count, None
