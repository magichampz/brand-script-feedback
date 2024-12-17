# feedback_processor.py
import json

def split_feedback(feedback, client):
    """
    Splits feedback into relevant sections.
    """
    # System message to set the behavior of the assistant
    system_prompt = (
        """
        You are a helpful assistant that separates client feedback into two sections: script feedback and video feedback.
        Your task is to process the input text and output the results in JSON format, clearly separating the two sections.

        - Script feedback: Include only feedback related to the script content (e.g., changes to lines, structure, tone, or messaging).
        - Video feedback: Include only instructions, reminders, or tips about video creation, screen recording, or other non-script-related tasks.

        If one of the sections does not have content, set it to `null`.

        Output the response as a JSON object with the following structure:

        {
            "script_feedback": "<content>",
            "video_feedback": "<content>"
        }
        """
    )
    
    user_message = (
        f"The client said: \"{feedback}\""
    )
    
    # We'll instruct the model to provide a short bullet point or sentence summarizing the key action.
    prompt = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=prompt,
        temperature=0.0,  # zero for more deterministic output
    )
    
    json_string = response.choices[0].message.content.strip()
    splits = json.loads(json_string)
    first_word = feedback.lower().split()[0]  # Get the first word in lowercase
    decision_map = {"approved": 1, "rejected": 0}  # Define the mapping
    splits["decision"] = decision_map.get(first_word, None)

    # Extract the assistant's final answer
    return splits


def extract_script_key_points_2(script_feedback, decision, client):
    """
    Extracts key points from the script feedback.
    """
    system_prompt = (
        """
        You are a helpful assistant that extracts actionable key points from the script feedback section. 
        Your task is to focus on summarizing the main instructions or requirements as a structured output, 
        organized by themes. 

        Each theme should represent the topic of the feedback, which should be a few words summarising what the feedback is about. (e.g., "Links and user engagement", "Overall value of the product", or the theme could be related to specific features of the product). 
        For each theme, list the key points as concise and actionable guidelines. Focus on the big-picture intent 
        of the feedback rather than quoting or paraphrasing specific phrases. there can be multiple themes discussed in the feedback message.

        Output the response as a structured JSON object with the following format:

        {
            "Theme 1": ["Key point 1", "Key point 2"],
            "Theme 2": ["Key point 3", "Key point 4"]
        }

        If there is only one theme, structure the output with a single key-value pair. If no feedback is provided, return an empty JSON object (`{}`).

        Example 1:

        Input:
        The script looks great and I am happy to approve it. Great work!!
        Just one small note: where you say ""But don’t take my word for it, give Milanote a go for your next project and experience it for yourself!"" can you please add a line saying something along the lines of ""I have added a link for you in the description box"". It would help to have a CTA in the middle of the video as well.

        Output:
        {
            "Links and user engagement": [
                "Mention the link in the description box.",
                "Include a CTA during the video."
            ]
        }
        
        Example 2:
        
        Input:
        Just one small note: Where you say "whether you're a crochet designer or fashion designer, Milanote makes starting a new project........", could you please change that to "whether you're a crochet designer or fashion designer or a creative in general, Milanote makes starting a new project....." because we don't want the audience to get confused and think that Milanote is just limited to fashion projects.
        
        Output:
        {
            "Milanote use cases": [
                "Don't make it seem like Milanote only caters to certain projects, as it is a tool for all creative work."
            ]
        }
        
        
        Remember:
        - Identify the theme(s) of the feedback based on the main ideas.
        - Focus on the intent, themes, or high-level suggestions behind the feedback.
        - Group actionable points under their respective themes as lists.
        - Avoid quoting specific phrases or rewording client-provided text.
        - Keep responses concise, actionable, and focused on what the reviewer needs to know.
        """
    )
    
    # The user's feedback message
    user_message = (
        f"Script feedback: \"{script_feedback}\""
    )
    
    # We'll instruct the model to provide a short bullet point or sentence summarizing the key action.
    prompt = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=prompt,
        temperature=0.0,  # zero for more deterministic output
    )
    
    json_string = response.choices[0].message.content.strip()
    themes_and_points = json.loads(json_string)
    
    structured_output = {
        theme: {
            "key_points": points,
            "decision": decision
        }
        for theme, points in themes_and_points.items()
    }
    
    # Extract the assistant's final answer
    return structured_output


def consolidate_feedbacks(feedback_list):
    """
    Consolidates feedback entries into a structured format.
    """
    consolidated_feedback = {}
    
    for i, feedback in enumerate(feedback_list):
        splits = split_feedback(feedback)
        
        if "script_feedback" in splits:
            key_points = extract_script_key_points_2(splits["script_feedback"], splits["decision"])
            for theme, data in key_points.items():
                if theme not in consolidated_feedback:
                    consolidated_feedback[theme] = {
                        "key_points": [],
                        "decision": data["decision"]
                    }
                # Merge key points, avoiding duplicates
                consolidated_feedback[theme]["key_points"].extend(data["key_points"])
                consolidated_feedback[theme]["key_points"] = list(set(consolidated_feedback[theme]["key_points"]))
    
    return consolidated_feedback


def summarize_feedback(consolidated_feedback, client):
    """
    Summarizes the consolidated feedback into a concise report.
    """
    feedback_input = json.dumps(consolidated_feedback, indent=4)
    
    # LLM prompt
    system_prompt = """
    You are a helpful assistant that summarizes feedback by identifying and merging similar points into a concise summary. 
    Your task is to analyze a list of key feedback points across multiple themes, remove repetitions, and combine similar ideas.
    Maintain the same JSON structure as the original input, which is specified below:
    
    {
        "Theme 1": {
            "key_points": ["Key point 1", "Key point 2"],
            "decision": 0
        },
        "Theme2": {
            "key_points": ["Key point 3", "Key point 4"],
            "decision": 1
        }
    }
    
    Pay attention to the decision value in each theme. If there are similar themes with different decisions, set the decision to 0.
    """
    user_message = feedback_input
    
    prompt = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=prompt,
        temperature=0.0,  # zero for more deterministic output
    )
    
    # Parse the response into a dictionary
    output = response.choices[0].message.content.strip()
    summarized_feedback = json.loads(output)
    
    return summarized_feedback


def generate_feedback_2nd(script, summarized_feedback, client):
    """
    Generates feedback based on the summarized feedback and script.
    """
    # LLM system prompt
    system_prompt = """
    You are a helpful assistant that reviews video scripts and provides feedback based on a set of feedback key points. 
    Your task is to:
    1. Analyze the video script and identify any relevant topics that match the provided feedback key points.
    2. If a key point does not match any part of the script, do not talk about that point. 
    3. Add actionable feedback only for areas where the script does not align with the feedback key points.
    4. Do not talk about more than 2 themes. The feedback needs to be concise

    Output the feedback in the following format:
    "Draft Script with Further Feedback"
    <insert feedback about the script here>

    """

    # Prepare user message
    user_message = f"""
    Script:
    {script}

    Feedback Key Points:
    {json.dumps(summarized_feedback, indent=4)}
    """

    # Prepare the LLM prompt
    prompt = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]

    # Call the LLM API
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=prompt,
        temperature=0.0,  # Zero for deterministic output
    )

    # Extract the LLM's response
    return response.choices[0].message.content.strip()