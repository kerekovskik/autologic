REASONING_MODULES_LIST = ["How could I devise an experiment to help solve that problem?"
,"Make a list of ideas for solving this problem, and apply them one by one to the problem to see if any progress can be made."
,"How could I measure progress on this problem?"
,"How can I simplify the problem so that it is easier to solve?"
,"What are the key assumptions underlying this problem?"
,"What are the potential risks and drawbacks of each solution?"
,"What are the alternative perspectives or viewpoints on this problem?"
,"What are the long-term implications of this problem and its solutions?"
,"How can I break down this problem into smaller, more manageable parts?"
,"Critical Thinking: This style involves analyzing the problem from different perspectives, questioning assumptions, and evaluating the evidence or information available. It focuses on logical reasoning, evidence-based decision-making, and identifying potential biases or flaws in thinking."
,"Try creative thinking, generate innovative and out-of-the-box ideas to solve the problem. Explore unconventional solutions, thinking beyond traditional boundaries, and encouraging imagination and originality."
,"Seek input and collaboration from others to solve the problem. Emphasize teamwork, open communication, and leveraging the diverse perspectives and expertise of a group to come up with effective solutions."
,"Use systems thinking: Consider the problem as part of a larger system and understanding the interconnectedness of various elements. Focuses on identifying the underlying causes, feedback loops, and interdependencies that influence the problem, and developing holistic solutions that address the system as a whole."
,"Use Risk Analysis: Evaluate potential risks, uncertainties, and tradeoffs associated with different solutions or approaches to a problem. Emphasize assessing the potential consequences and likelihood of success or failure, and making informed decisions based on a balanced analysis of risks and benefits."
,"Use Reflective Thinking: Step back from the problem, take the time for introspection and self-reflection. Examine personal biases, assumptions, and mental models that may influence problem-solving, and being open to learning from past experiences to improve future approaches."
,"What is the core issue or problem that needs to be addressed?"
,"What are the underlying causes or factors contributing to the problem?"
,"Are there any potential solutions or strategies that have been tried before? If yes, what were the outcomes and lessons learned?"
,"What are the potential obstacles or challenges that might arise in solving this problem?"
,"Are there any relevant data or information that can provide insights into the problem? If yes, what data sources are available, and how can they be analyzed?"
,"Are there any stakeholders or individuals who are directly affected by the problem? What are their perspectives and needs?"
,"What resources (financial, human, technological, etc.) are needed to tackle the problem effectively?"
,"How can progress or success in solving the problem be measured or evaluated?"
,"What indicators or metrics can be used?"
,"Is the problem a technical or practical one that requires a specific expertise or skill set? Or is it more of a conceptual or theoretical problem?"
,"Does the problem involve a physical constraint, such as limited resources, infrastructure, or space?"
,"Is the problem related to human behavior, such as a social, cultural, or psychological issue?"
,"Does the problem involve decision-making or planning, where choices need to be made under uncertainty or with competing objectives?"
,"Is the problem an analytical one that requires data analysis, modeling, or optimization techniques?"
,"Is the problem a design challenge that requires creative solutions and innovation?"
,"Does the problem require addressing systemic or structural issues rather than just individual instances?"
,"Is the problem time-sensitive or urgent, requiring immediate attention and action?"
,"What kinds of solution typically are produced for this kind of problem specification?"
,"Given the problem specification and the current best solution, have a guess about other possible solutions."
,"Let’s imagine the current best solution is totally wrong, what other ways are there to think about the problem specification?"
,"What is the best way to modify this current best solution, given what you know about these kinds of problem specification?"
,"Ignoring the current best solution, create an entirely new solution to the problem."
,"Let’s think step by step."
,"Let’s make a step by step plan and implement it with good notion and explanation."
]

SELECT_PHASE_PROMPT_TEMPLATE = """# Instructions
For the given task, you are to select 1 to 5 Reasoning Modules which are crucial to utilize in order to solve the given task.

## Task 

{task}

## Reasoning Modules

{modules}

## Detailed Instructions

The reasoning modules have been listed above. 
Your answer should include only the number associated with the associated Reasoning Module in a list stored in a field called "reasoning_modules" in a JSON object. 
Your answer should be in a JSON code block.

## Output example

```json
{{
    "reasoning_modules": [1, 15, 32]
}}
```
"""

ADAPT_PHASE_PROMPT_TEMPLATE = """# Given Reasoning Modules

{modules}

# Given Task 

{task}

# Detailed Instruction 

Your need to Rephrase and specify each given reasoning module so that it better helps to solve the given task and its verbiage is task specific.
Your answer should be in a markdown code block as shown in the example. The markdown codeblock should be enclosed in triple back-tick notation with the md language specifier.
Each rephrased reasoning module should be its own list item but it can include sub-lists, etc.

### Example Task 

John has 12 apples. He gives 5 apples to his sister. If he finds 8 more apples, how many apples does he have in total?

### Given Reasoning Modules 

- Make a list of ideas for solving this problem, and apply them one by one to the problem to see if any progress can be made.
- What is the core issue or problem that needs to be addressed?
- What kinds of solution typically are produced for this kind of problem specification?

### Example rephrasing

```md
- Break down the arithmetic operations involved in the problem: Start by identifying the initial number of apples John has, then subtract the number given to his sister, and finally add the number of apples found later.
- Identify the core arithmetic operation required to solve the problem: Determine the sequence of addition and subtraction needed to calculate the total number of apples John ends up with.
- Consider common mathematical operations applied in similar problems: Recognize that this problem involves basic arithmetic operations—specifically, subtraction followed by addition—to find the total count of items.
```

"""

IMPLEMENT_PHASE_PROMPT_TEMPLATE = """# Given Task

{task}

# Given Reasoning Modules

{modules}

## Example Task 

John has 12 apples. He gives 5 apples to his sister. If he finds 8 more apples, how many apples does he have in total?

## Example Reasoning Modules

- Break down the arithmetic operations involved in the problem: Start by identifying the initial number of apples John has, then subtract the number given to his sister, and finally add the number of apples found later.
- Identify the core arithmetic operation required to solve the problem: Determine the sequence of addition and subtraction needed to calculate the total number of apples John ends up with.
- Consider common mathematical operations applied in similar problems: Recognize that this problem involves basic arithmetic operations—specifically, subtraction followed by addition—to find the total count of items.

## Example Reasoning Structure Output:

```json
{{
  "Reasoning Structure": {{
    "Step 1: Identify Initial Quantity": {{
      "Description": "John starts with a certain number of apples.",
      "Action": "Identify initial number of apples John has.",
      "Initial Quantity": ""
    }},
    "Step 2: Subtract Quantity Given Away": {{
      "Description": "John gives some apples to his sister.",
      "Action": "Subtract the number of apples given to his sister from the initial count.",
      "Quantity Given Away": "5 apples",
      "Effect on Total": ""
    }},
    "Step 3: Add Quantity Found": {{
      "Description": "John finds additional apples.",
      "Action": "Add the number of apples found to the current total.",
      "Quantity Found": "8 apples",
      "Effect on Total": ""
    }},
    "Step 4: Calculate Final Quantity": {{
      "Description": "Calculate the final count of apples John has.",
      "Action": "Apply the sequence of subtraction and addition to the initial count.",
      "Core Operations": "Subtraction followed by addition",
      "Final Total": ""
    }},
    "Considerations": {{
      "Common Mathematical Operations": "This problem involves basic arithmetic operations (subtraction, addition) commonly applied in similar scenarios.",
      "Problem-Solving Strategy": "Break down the problem into a series of arithmetic operations and execute them in sequence to find the total count."
    }},
    "FINAL_ANSWER": ""
  }}
}}
```

# Detailed instructions 

The reasoning modules have been listed above. 
Your job is to create a JSON formatted reasoning structure that implements the given reasoning modules for the given task but not to solve the given task. 
The given task will be solved by someone else using the reasoning structure that you construct.
Refer to the Example Reasoning Structure as an example of what a good comprehensive reasoning structure looks like. 
You have also been provided the example reasoning modules that go along with the example reasoning structure for reference.
Your answer should be in a JSON code block similar to the "Example Reasoning Structure Output" section. The JSON code block should use the triple back-tick notation as shown.
The reasoning structure should be formatted as key-value pairs. The Key should represent a reasoning step within the reasoning structure and the value should be left as a blank string.
The reasoning structure can be nested as deeply as needed to accurately spell out the reasoning steps required. 
The reasoning structure must contain a key called "FINAL_ANSWER" at the root level of the JSON sturucture with a blank string as the value. Ensure that the "FINAL_ANSWER" key is at the very bottom (is the last field) of the JSON structure.
"""

SOLVE_PROMPT_TEMPLATE = """ # Given Reasoning Structure

```json
{reasoning_structure}
```

# Given Task

{task}

## Example Output 

```json
{{
  ...
}}
```

# Detailed Instructions 

You must use the given REASONING STRUCTURE to solve the GIVEN TASK, both are provided above.
The REASONING STRUCTURE will guide your answer for the GIVEN TASK. 
You must fill out ALL of the empty strings on the value side of the key-value pairs in the JSON structure of the REASONING STRUCTURE.
Your output will consist of one codeblock. The codeblock will be a json codeblock enclosed by triple back-ticks with the json language specificer as shown in the "Example Output".
The json codeblock will contain the completely filled out reasoning structure.
"""