

# autologic

autologic is a Python package that implements the SELF-DISCOVER framework proposed in the paper ["SELF-DISCOVER: Large Language Models Self-Compose Reasoning Structures".](https://arxiv.org/abs/2402.03620) 

It provides a way for large language models (LLMs) to automatically compose modular reasoning structures to tackle complex reasoning tasks, without the need for training data or labels.
## Key Features

- Implements the full SELF-DISCOVER pipeline enabling LLMs to self-discover reasoning structures
- Works with Gemini Pro and local GGUF models via llama-cpp-python
- Flexible integration powered by a simple LLMConfig
- Interactive prompts or standalone execution
- CLI and Python API access

## Framework Overview

The SELF-DISCOVER framework consists of two key stages:

Stage 1: Self-discover a reasoning structure for the task from a set of seed "reasoning modules"

Stage 2: Solve instances by following the composed structure

The first stage has 3 steps guided by meta-prompting:

1. SELECT relevant reasoning modules
2. ADAPT modules to be task-specific
3. IMPLEMENT structure with adapted modules

## Getting Started

### Installation as editable package

The following instructions show the CMAKE arguments for compiling llama-cpp-python dependencies with support for metal.
Refer to https://github.com/abetlen/llama-cpp-python for instructions regarding different GPUs.

```bash
git clone https://github.com/waszumteufel/autologic.git
cd autologic
python3 -m venv venv
source  venv/bin/activate
CMAKE_ARGS="-DLLAMA_METAL=on" pip3 install -e .
```

### Directly install from Github

```bash
python3 -m venv venv
source  venv/bin/activate
CMAKE_ARGS="-DLLAMA_METAL=on" pip3 install git+https://github.com/waszumteufel/autologic@main#egg=autologic
```


## Configuration

### Gemini API Key

To use the Gemini model, set the `GEMINI_PRO_API_KEY` variable:

```
GEMINI_PRO_API_KEY="sk-..."
```

If this is not set, `solve()` will automatically read it from the `.env` file in the working directory or general environment.

### Environment Variables 

It is recommended to set sensitive values like API keys in a `.env` file.

This will be automatically loaded from the current working directory if present, and used to populate any unset configuration values that have matching environment variable names (i.e. `GEMINI_PRO_API_KEY`).

See the "Configuration" section of the documentation for the full set of options. Using `.env` and environment variables allows keeping credentials secure.

This allows conveniently configuring API keys and other settings without exposing them directly in code. The `LLMConfig` can then be initialized without explicitly passing these values every time.

## Usage

### Import and call the top-level solve() method:

#### Mixtral Example with the Python API 
The below code block illustrates how to use the Python API to use SELF-DISCOVER with a Mixtral GGUF.

```python
from autologic import reasoningEngine

my_config = reasoningEngine.LLMConfig(
        gguf_path="/tmp/mixtral-8x7b-instruct-v0.1.Q8_0.gguf",
        context_length=8000,
        model_type=reasoningEngine.ModelType.LOCAL,
        temp=0.2,
        chat_template=reasoningEngine.ChatTemplate.MIXTRAL_INSTRUCT,
        threads=12
    )

result = reasoningEngine.solve(task = "What is 2 + 2?", llmConfig=my_config)
print(result)
```
#### Gemini Pro Example with the Python API

The API Key for Gemini Pro is read from the `GEMINI_PRO_API_KEY` environment variable or .env file. It can optionally be passed in to through the `autologic.reasoningEngine.LLMConfig.api_key` field.

```python
from autologic import reasoningEngine

my_config = reasoningEngine.LLMConfig(
        context_length=8000,
        model_type=reasoningEngine.ModelType.GEMINI,
        temp=0.2,
    )
result = reasoningEngine.solve(task = "What is 2 + 2?", llmConfig=my_config)
print(result)
```

### Or use the CLI:

#### CLI Usage with a prompt

##### Gemini Pro example with CLI

Example with a prompt 

```bash
autologic gemini --temp 0.2 \
--retries 3 \
--prompt "What weighs more? A pound of feathers or a pound of lead?"
```

Example output 


```
Thinking...
2024-02-14 18:50:34.054248 | Starting SELECT Phase
2024-02-14 18:50:37.008261 | SELECT Phase Complete
2024-02-14 18:50:37.008367 | Starting ADAPT Phase
2024-02-14 18:50:40.322604 | ADAPT Phase Complete
2024-02-14 18:50:40.322641 | Starting IMPLEMENT Phase
2024-02-14 18:50:45.567405 | IMPLEMENT Phase Complete
2024-02-14 18:50:45.567738 | Starting to Solve Problem using Reasoning Structure
2024-02-14 18:50:52.775653 | Solution has been found.


ANSWER: The weight of a pound of feathers is equal to the weight of a pound of lead.
```

##### Qwen1.5 72B example with CLI

The below example shows how to specify a path to a GGUF model and how to specify the prompt format for the given model with the `--format` flag.
The example also showcases the usage of the `--verbose` flag which shows detailed reasoning information as well as the reasoning structure that the LLM self-discovers for the given problem.

```bash
autologic local --temp 0.2 \
--retries 5 \
--prompt "What weighs more? A pound of feathers or a pound of lead?" \
--gguf_path /tmp/qwen1_5-72b-chat-q5_k_m.gguf \
--threads 12 \
--layers -1 \
--format chatml \
--verbose  
```

Example output:

```
Thinking...
2024-02-14 20:05:23.116629 | Starting SELECT Phase
2024-02-14 20:06:41.595659 | SELECT Phase Complete
2024-02-14 20:06:41.595711 | Reasoning Modules Picked:
- 3. How can I simplify the problem so that it is easier to solve?
- 9. Critical Thinking: This style involves analyzing the problem from different perspectives, questioning assumptions, and evaluating the evidence or information available. It focuses on logical reasoning, evidence-based decision-making, and identifying potential biases or flaws in thinking.
- 16. What are the underlying causes or factors contributing to the problem?
- 22. How can progress or success in solving the problem be measured or evaluated?
- 23. What indicators or metrics can be used?

2024-02-14 20:06:41.595719 | Starting ADAPT Phase
2024-02-14 20:07:22.370683 | ADAPT Phase Complete
2024-02-14 20:07:22.370713 | Task-specific Reasoning Module verbiage:
- Clarify the units and equalities: Both items are measured in pounds, which means they weigh the same amount by definition; a pound is a unit of weight or mass.
- Understand the context and potential misconceptions: The question is a classic example of a trick question, as some may think lead is denser and therefore heavier, but in reality, both weigh the same.
- Address the physical properties without affecting the weight: While lead is denser than feathers, density does not affect the weight for the same volume; both weigh one pound, regardless of their density.

2024-02-14 20:07:22.370720 | Starting IMPLEMENT Phase
2024-02-14 20:08:46.753718 | IMPLEMENT Phase Complete
2024-02-14 20:08:46.753805 | Reasoning Structure:
{
  "Reasoning Structure": {
    "Step 1: Understand the Weighing Units": {
      "Description": "Both items are measured in the same unit.",
      "Action": "Confirm that both 'pound of feathers' and 'pound of lead' use the same unit (pound).",
      "Unit": "pound"
    },
    "Step 2: Recognize the Trick Question": {
      "Description": "The question is designed to prompt a misconception.",
      "Action": "Identify that some might think density affects weight, but it doesn't for the same volume.",
      "Misconception": "Density affects weight"
    },
    "Step 3: Define Density": {
      "Description": "Density is mass per unit volume.",
      "Action": "Explain that density does not change the weight for the same amount of mass.",
      "Density": "mass / volume"
    },
    "Step 4: Compare Weights Without Density": {
      "Description": "Focus on the weight aspect.",
      "Action": "Since both weigh one pound, compare them without considering density.",
      "Comparison": "Equal weight"
    },
    "Step 5: Conclusion": {
      "Description": "Both weigh the same amount.",
      "Action": "Both a pound of feathers and a pound of lead weigh the same.",
      "Final Conclusion": ""
    },
    "FINAL_ANSWER": ""
  }
}
2024-02-14 20:08:46.753961 | Starting to Solve Problem using Reasoning Structure
2024-02-14 20:10:07.283210 | Problem Solved
Completed Reasoning Structure:
{
  "Reasoning Structure": {
    "Step 1: Understand the Weighing Units": {
      "Description": "Both items are measured in the same unit.",
      "Action": "Confirm that both 'pound of feathers' and 'pound of lead' use the same unit (pound).",
      "Unit": "pound"
    },
    "Step 2: Recognize the Trick Question": {
      "Description": "The question is designed to prompt a misconception.",
      "Action": "Identify that some might think density affects weight, but it doesn't for the same volume.",
      "Misconception": "Density affects weight"
    },
    "Step 3: Define Density": {
      "Description": "Density is mass per unit volume.",
      "Action": "Explain that density does not change the weight for the same amount of mass.",
      "Density": "mass / volume"
    },
    "Step 4: Compare Weights Without Density": {
      "Description": "Focus on the weight aspect.",
      "Action": "Since both weigh one pound, compare them without considering density.",
      "Comparison": "Equal weight"
    },
    "Step 5: Conclusion": {
      "Description": "Both weigh the same amount.",
      "Action": "Both a pound of feathers and a pound of lead weigh the same.",
      "Final Conclusion": "A pound of feathers and a pound of lead weigh equally."
    },
    "FINAL_ANSWER": "A pound of feathers and a pound of lead weigh equally."
  }
}
2024-02-14 20:10:07.283302 | Solution has been found.


ANSWER: A pound of feathers and a pound of lead weigh equally.
```

#### Interactive CLI Mode


The CLI can be invoked without passing a `--prompt` argument to enter an interactive mode. This allows conveniently sending multi-line prompts for the model to reason over:

```bash
% autologic gemini --temp 0.2

Entering Interactive Mode: CTRL + C to send multi-line input. CTRL + D to exit the program.
> 
```

After starting interactive mode, you will be prompted to enter text:

```bash
Entering Interactive Mode: CTRL + C to send multi-line input. CTRL + D to exit the program.
> What weighs more?  
> A pound of feathers?
> Or a pound of lead?
> 
```
Enter your reasoning prompt spanning multiple lines.

To submit the prompt, press **CTRL + C** to send the input while staying in interactive mode.

This will trigger the model to start reasoning over the prompt:

```
> What weighs more?
> a pound of feathers or 
> a pound of lead?
> ^C
Thinking...
2024-02-14 20:17:38.307588 | Starting SELECT Phase
2024-02-14 20:17:42.403366 | SELECT Phase Complete
2024-02-14 20:17:42.403473 | Starting ADAPT Phase
2024-02-14 20:17:45.680310 | ADAPT Phase Complete
2024-02-14 20:17:45.680418 | Starting IMPLEMENT Phase
2024-02-14 20:17:52.029561 | IMPLEMENT Phase Complete
2024-02-14 20:17:52.029897 | Starting to Solve Problem using Reasoning Structure
2024-02-14 20:17:57.064476 | Solution has been found.


ANSWER: A pound of feathers weighs the same as a pound of lead.
```

Once you are done, send the **CTRL + D** signal to exit interactive mode and quit the CLI program.

```
> Goodbye!
```

This interactive workflow allows you to conveniently test long, complex reasoning without having to put all the prompt in quotes or escape newlines.

## TODO
- Expose information on Reasoning Structure and Reasoning Module selection via Python API. Currently, it is only visible when using verbose=True in CLI and API. 
- Add Mixed mode where discovery of Reasoning Structure and usage of Reasoning Structure can be done by different LLMs.
- Add support for openai models
- Add package to Pypi
- Add support for other prompt formats (Llama2, airoboros, etc.)
- Add REST support via Flask
