# What's in the Kitchen Sink? Creating LLM Agents with the Tree of Thoughts Framework

There are currently a number of well-known LLM "Agents" based on the ReAct framework. For these agents, problem-solving capabilities start with outlining a set of 'tasks' in the form of thoughts, following a linear path through a chain of thoughts until task completion. While interesting to observe, this approach rarely leads to a functional result on complex or multi-step problems. 

Simple react agents like Auto-GPT and Baby-AGI lack the ability to self-supervise, correct course, or respond to new information and changing circumstances as a human would when solving a complex task. This project aims to develop a new type of agent, not based on ReAct or COT, but based off a more recent framework called "Tree of Thoughts" (ToT) as suggested in "Tree of Thoughts: Deliberate Problem Solving with Large Language Models" by Yao et. al.

## The Tree of Thoughts Framework

ToT is essentially a chain of thought prompting with recursion. This more sophisticated method allows an agent to traverse down multiple branches of a complex problem, continually re-planning each node by further fleshing out and defining tasks before returning a result which is then passed to the next branch of action. Running memory is used to share the result of each node with downstream nodes.

## The Kitchen Sink Agent

The Kitchen Sink agent uses all of these techniques, at various times, to tune the accuracy of LLM responses. It is not just one agent, but four, each running asynchronously as needed to complete tasks. These agent personas interact with each other, supervising each other's work and providing necessary process inputs. 

Here are the four agent personas:

1. **The Supervisor** - Reviews the current task (parent leaf) and defines the success criteria to determine if the goal is met.
2. **The Planner** - Thinks about what to do and breaks each task into a set of thoughts preceded by "I Need To…" 
3. **The Designer** - Reviews the goal and creates N number of design options for a deliverable.
4. **The Executor** - Creates output from a specification with a description of deliverables, success criteria, and steps to completion from the designer.

## Does It Work?

Yes! Despite a few challenges related to using GPT 3.5 rather than GPT 4.0, the process happily returns usable code files. 

## Improvements and Next Steps

1. Reduce the number of evaluation prompts.
2. Add a UI to outline the visual form of the tree and its progress.
3. Implement size limitations on the prompts to prevent token overflow errors.
4. Expand the executor toolbox with more tools for deliverable evaluation.

## Get Involved

All of the actual prompts and code for this agent are publicly available in this repository. Feel free to run this in Python if you'd like - the main process should be executed from "Plan" (run plan.py). The input is loaded in the "test_dictionary". If you'd like to help make it better, submit a PR and let's chat!

## References

- [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)
- [Tree of Thoughts paper](https://arxiv.org/abs/2305.10601)
- [Teaching large language models to self-debug](https://arxiv.org/pdf/2304.05128.pdf)
- [Language Models as Zero-Shot Planners](https://arxiv.org/pdf/2201.07207.pdf)
- [Extracting Actionable Knowledge for Embodied Agents](https://arxiv.org/pdf/2201.
