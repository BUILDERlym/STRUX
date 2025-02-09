# SUMMARIZE_INSTRUCTION = """Given a segment of executive speech from the earnings call, which may be from the Prepared Remarks session or the executives' responses in the Q&A session, summarize key facts regarding {ticker} stock. Note that for the Q&A session, the segment contains only the executives' responses, not the analysts' questions. Follow these guidelines:

# 1. You MUST extract NO MORE than {words_category} key facts.
# 2. Focus on information that could impact stock price, such as:
#    - Financial performance and clarifications
#    - Future outlook and guidance
#    - Strategic decisions and company direction
#    - Market trends and competitive positioning
#    - New products or services
#    - Responses to industry challenges or opportunities
# 3. Present each fact DIRECTLY without numbering or other punctuation marks.
# 4. Ensure that the facts are objective and based solely on the information provided in the transcript.
# 5. For executive responses in the Q&A session, infer the context of the executive's answer even though the analyst's question is not provided.

# **Examples:**

# **Example 1 (Prepared Remarks):**

# Earnings call transcript:

# "name": "John Smith, CEO",
# "speech": [
#     "Thank you, everyone, for joining us today. I'm pleased to report that our Q4 results exceeded expectations, with revenue growing 15% year-over-year to $2.5 billion. This growth was primarily driven by strong performance in our cloud services division, which saw a 30% increase in revenue.",
#     "However, we faced some challenges in our hardware segment, where revenue declined by 5% due to supply chain disruptions. We're actively working to mitigate these issues and expect improvements in the coming quarters.",
#     "Looking ahead, we're excited about the launch of our new AI-powered platform next month, which we believe will open up significant opportunities in the enterprise market. We're also continuing to invest heavily in R&D, with a focus on sustainable technologies that we believe will drive long-term growth.",
#     "In terms of guidance, we're projecting revenue growth of 10-12% for the next quarter, which is slightly below analyst estimates due to ongoing macroeconomic uncertainties."
# ]

# Facts:
# Company reported Q4 revenue of $2.5 billion, a 15% year-over-year increase, exceeding expectations.
# Cloud services division saw a 30% increase in revenue, driving overall growth.
# Hardware segment revenue declined by 5% due to supply chain disruptions.
# New AI-powered platform launching next month expected to create significant opportunities in the enterprise market.
# Company is investing heavily in R&D, focusing on sustainable technologies for long-term growth.
# Guidance for next quarter projects 10-12% revenue growth, slightly below analyst estimates.

# **Example 2 (Q&A Session):**

# Earnings call transcript:

# "name": "John Smith, CEO",
# "speech": [
#     "The 5% decline in our hardware segment was primarily due to semiconductor shortages affecting our production capacity. We've already secured new suppliers and expect to resolve most of these issues by the end of next quarter. In fact, we anticipate returning to growth in this segment by Q3."
# ]

# Facts:
# Hardware segment declined 5% due to semiconductor shortages; new suppliers secured, issues expected to be resolved by next quarter end.
# Anticipate returning to growth in hardware segment by Q3.

# Earnings call transcript:
# {segments}

# Facts:"""


# # PREDICT_INSTRUCTION = """Given a table of facts about {ticker}, predict the long-term stock recommendation for {ticker}. Follow these steps:

# # 1. Select 6-10 most relevant facts from the provided fact table. Ensure a balance between positive, and negative facts.
# # 2. Assign an impact strength to each selected fact:
# #    - Use '+' for positive impact (more '+' signs indicate stronger positive impact, up to '+++')
# #    - Use '-' for negative impact (more '-' signs indicate stronger negative impact, up to '---')
# # 3. Focus on factors that could affect the stock price in the long term.
# # 4. Weigh both the quantitative (number and strength of impacts) and qualitative (relevance and importance) aspects of the facts.
# # 5. Synthesize all factors to form a view on the likely long-term price movement.

# # Based on your analysis, you MUST choose one of these five recommendations:
# # a) Strongly Buy
# # b) Buy
# # c) Hold
# # d) Sell
# # e) Strongly Sell

# # You MUST choose one of these five options. No other responses are acceptable.

# # You MUST provide your response EXACTLY in this format:
# # Selected Facts with Assigned Strength:
# #    - [Fact 1]|[Content] : [Assigned strength]
# #    - [Fact 2]|[Content] : [Assigned strength]
# #    ...
# #    (List 6-10 facts with their assigned strengths)

# # Recommendation: [Strongly Buy / Buy / Hold / Sell / Strongly Sell]

# # Justification: [Your concise reasoning in one paragraph, focusing on key long-term factors]

# # {summary}
# # """

# PREDICT_INSTRUCTION = """Given a table of facts about {ticker}, predict the long-term stock recommendation for {ticker}. Your task is to provide an unbiased, objective analysis considering all possible outcomes. Follow these steps:

# 1. Select 6-10 most relevant facts from the provided fact table. Ensure a balance between positive and negative facts.
# 2. Assign an impact strength to each selected fact:
#    - Use '+' for positive impact (more '+' signs indicate stronger positive impact, up to '+++')
#    - Use '-' for negative impact (more '-' signs indicate stronger negative impact, up to '---')
# 3. Focus on factors that could affect the stock price in the long term (after 30 trading days).
# 4. Weigh both the quantitative (number and strength of impacts) and qualitative (relevance and importance) aspects of the facts.
# 5. Consider potential risks and negative scenarios, even if they are not explicitly stated in the facts.
# 6. Analyze how the selected facts might interact or compound each other.
# 7. Compare the current situation with historical patterns or industry benchmarks, if applicable.
# 8. Synthesize all factors to form a view on the likely long-term price movement, considering both upside potential and downside risks.

# The Fact Table is summarized from earnings call, thus may appear more positive than the actual situation.

# Based on your analysis, you MUST choose one of these five recommendations:
# a) Strongly Buy
# b) Buy
# c) Hold
# d) Sell
# e) Strongly Sell

# You MUST choose one of these five options. No other responses are acceptable. Be prepared to recommend any of these options if the analysis warrants it.

# You MUST provide your response EXACTLY in this format:
# Selected Facts with Assigned Strength:
#    - Fact [number] | [Content]: [Assigned strength]
#    - [Continue for all selected facts]

# Recommendation: [Strongly Buy / Buy / Hold / Sell / Strongly Sell]

# Justification: [Your concise reasoning in short sentences, focusing on key long-term factors. Explicitly address both positive and negative aspects, and explain why your chosen recommendation is more appropriate than the others.]

# Facts Table:
# {summary}
# """

# # PREDICT_INSTRUCTION = """Given a table of facts about {ticker}, predict the stock recommendation for {ticker}. Your task is to provide an unbiased, objective analysis considering all possible outcomes. Follow these steps:

# # 1. Select 6-10 most relevant facts from the provided fact table. Ensure a balance between positive and negative facts.
# # 2. Assign an impact strength to each selected fact:
# #    - Use '+' for positive impact (more '+' signs indicate stronger positive impact, up to '+++')
# #    - Use '-' for negative impact (more '-' signs indicate stronger negative impact, up to '---')

# # Based on your analysis, you MUST choose one of these five recommendations:
# # a) Strongly Buy
# # b) Buy
# # c) Hold
# # d) Sell
# # e) Strongly Sell

# # You MUST choose one of these five options. No other responses are acceptable. Be prepared to recommend any of these options if the analysis warrants it.

# # You MUST provide your response EXACTLY in this format:
# # Selected Facts with Assigned Strength:
# #    - Fact [number] | [Content]: [Assigned strength]
# #    - [Continue for all selected facts]

# # Recommendation: [Strongly Buy / Buy / Hold / Sell / Strongly Sell]

# # Justification: [Your concise reasoning in short sentences.]

# # Facts Table:
# # {summary}
# # """

# REFLECT_INSTRUCTION = """
# =======================
# You are an advanced reasoning agent capable of improving through self-reflection. You were previously given a table of facts about {ticker} stock, from which you selected facts, assigned strengths to provide a recommendation and a corresponding justification. Your previous assessments were unsuccessful, resulting in WRONG stock RECOMMENDATIONS.

# Your task is to reflect on the previous trials and suggest significant improvements. Review the original facts table, your previous selections of facts, their assigned strengths, and your reasoning critically. Identify major issues in your fact selection, strength assignment, or reasoning process.

# You MUST adhere EXACTLY to the format specified below. Any deviation from this format will be considered incorrect. Your new recommendation MUST be different from all previous ones and based solely on your analysis of the facts, not on any predefined pattern.
# =======================
# INPUT:

# Facts Table:
# [Full facts table will be provided here]

# Previous Incorrect Outputs:
# [A list of previous incorrect outputs, including selected facts, strengths, recommendations, and justifications]

# =======================
# OUTPUT:

# Selected Facts with Assigned Strength:
#    - Fact [number] | [Content]: [strength]
#    - [Continue for all selected facts, ensuring 6-10 facts are chosen]

# Recommendation: [Your new recommendation MUST be different from all previous ones and based on your analysis: Strongly Buy / Buy / Hold / Sell / Strongly Sell]

# Justification: [Provide a concise explanation for your changes and new recommendation in one paragraph. Focus on how your analysis of the facts led to this different conclusion, and how you've addressed the errors in previous assessments]

# =======================
# INPUT:
# {Facts_Table}
# The following are outputs that contain incorrect recommendations from previous trials, possibly with incorrect selected facts, and incorrect assigned strength.

# {scratchpad}

# OUTPUT:
# """


SUMMARIZE_INSTRUCTION = """You have been given an executive's speech from an earnings call transcript. This could be from the Prepared Remarks segment or from responses given during the Q&A session. Your task is to summarize the essential details related to {ticker} stock.

1. Keep your summary concise, with no more than {words_category} key facts. 
2. Focus on significant details that could impact the stock price, including financial performance, future outlooks and guidance, strategic decisions and company direction, market trends and competitive positioning, introductions of new products or services, and responses to industry challenges and opportunities.
3. Present these facts clearly without using any numbering or special formatting. 
4. Make sure your summary remains factual and based solely on the content of the transcript. 

**Examples:**

**Example 1 (Prepared Remarks):**

Earnings call transcript:

"name": "John Smith, CEO",
"speech": [
    "Thank you, everyone, for joining us today. I'm pleased to report that our Q4 results exceeded expectations, with revenue growing 15% year-over-year to $2.5 billion. This growth was primarily driven by strong performance in our cloud services division, which saw a 30% increase in revenue.",
    "However, we faced some challenges in our hardware segment, where revenue declined by 5% due to supply chain disruptions. We're actively working to mitigate these issues and expect improvements in the coming quarters.",
    "Looking ahead, we're excited about the launch of our new AI-powered platform next month, which we believe will open up significant opportunities in the enterprise market. We're also continuing to invest heavily in R&D, with a focus on sustainable technologies that we believe will drive long-term growth.",
    "In terms of guidance, we're projecting revenue growth of 10-12% for the next quarter, which is slightly below analyst estimates due to ongoing macroeconomic uncertainties."
]

Facts:
Company reported Q4 revenue of $2.5 billion, a 15% year-over-year increase, exceeding expectations.
Cloud services division saw a 30% increase in revenue, driving overall growth.
Hardware segment revenue declined by 5% due to supply chain disruptions.
New AI-powered platform launching next month expected to create significant opportunities in the enterprise market.
Company is investing heavily in R&D, focusing on sustainable technologies for long-term growth.
Guidance for next quarter projects 10-12% revenue growth, slightly below analyst estimates.

**Example 2 (Q&A Session):**

Earnings call transcript:

"name": "John Smith, CEO",
"speech": [
    "The 5% decline in our hardware segment was primarily due to semiconductor shortages affecting our production capacity. We've already secured new suppliers and expect to resolve most of these issues by the end of next quarter. In fact, we anticipate returning to growth in this segment by Q3."
]

Facts:
Hardware segment declined 5% due to semiconductor shortages; new suppliers secured, issues expected to be resolved by next quarter end.
Anticipate returning to growth in hardware segment by Q3.

Earnings call transcript:
{segments}

Facts:"""


PREDICT_INSTRUCTION = """Your task is to make an investment decision by predicting the post-earnings stock movement trend for {ticker} over a 30-day period. Use the provided fact table and follow these steps:

1. Choose 6-10 of the most relevant facts from the table. Make sure there is a balance between positive and negative facts.

2. Each selected fact needs to be assessed for its likely impact on the stock's price:
   - Use a '+' symbol to denote a positive impact. The number of '+' symbols can vary from one ('+') to three ('+++') depending on the increasing strength of the positive impact.
   - Use a '-' symbol to denote a negative impact. Similarly, the number of '-' signs can range from one ('-') to three ('---') based on the severity of the negative impact.

3. Prioritize facts that could influence the stock price over the long term.

4. Evaluate the facts based on both the quantitative (impact strengths) and qualitative (relevance and importance) aspects of each fact.

5. Combine and analyze all the selected facts to predict the likely direction of the stock price movement.

Your response must be formatted as follows:

Selected Facts with Assigned Strength:
   - Fact [number] | [Content]: [Assigned Strength]
   ...
   (Include between 6-10 facts with their assigned strengths)

Decision: [Choose one: Strongly Buy, Buy, Hold, Sell, Strongly Sell. Please note that no other responses will be considered valid.]

Justification: [Provide a concise paragraph summarizing your reasoning, focusing on key facts that influence your decision.]

Fact Table: 
{fact_table}
"""


REFLECT_INSTRUCTION = """
You are an advanced reasoning agent capable of enhancing your capabilities through self-reflection. In a previous task, you analyzed a fact table related to a specific stock. You selected various facts from the table, assigned impacts and strengths to them, and formulated a stock investment decision along with supporting justifications. Unfortunately, your assessments led to an incorrect stock investment decision.

Your current task is to critically review your prior efforts. You must reexamine the original fact table, the facts you previously selected, the strengths you assigned to each, and the reasoning behind your conclusions. It is essential to identify significant flaws in your selection of facts, the assignment of their strengths, or in the reasoning process you employed.

You must adhere to the following format in your analysis and only present the new OUTPUT part. Any deviation from this format will render it invalid. Your new stock investment decision should differ from all previous ones and should be derived exclusively from a detailed analysis of the provided facts, without relying on any pre-existing patterns.

========
INPUT:

Fact Table: 
[The full fact table will be provided here]

Previous Incorrect Outputs: 
[A list of previously incorrect outputs will be included here, containing selected facts, their assessed strengths, decisions, and the justifications provided for them.]

OUTPUT:

Selected Facts with Assigned Strength:
- Fact [number] | [Content]: [Assigned Strength]
- [This pattern will continue for each of the selected facts, ensuring that 6-10 facts are chosen.]

Decision: [Your new decision, which must be different from all previous decisions, will be one of the following: Strongly Buy, Buy, Hold, Sell, Strongly Sell.]

Justification:
[Provide a clear explanation for your updated changes and new decision in a single paragraph. Emphasize how your analysis of the facts led you to a different decision from previous outputs, and how you have addressed any errors found in prior assessments.]

========
INPUT: 

Fact Table:
{fact_table}

Previous Incorrect Outputs: The following list includes outputs from previous trials. This includes decisions that were incorrect, potentially incorrect facts that were selected, and inaccurately assigned strengths.
{previous_incorrect_outputs}

OUTPUT:
"""

PREDICT_INSTRUCTION_less = """Your task is to make an investment decision by predicting the post-earnings stock movement trend for {ticker} over a 30-day period. Use the provided fact table and follow these steps:

1. Choose 3-6 of the most relevant facts from the table. Make sure there is a balance between positive and negative facts.

2. Each selected fact needs to be assessed for its likely impact on the stock's price:
   - Use a '+' symbol to denote a positive impact. The number of '+' symbols can vary from one ('+') to three ('+++') depending on the increasing strength of the positive impact.
   - Use a '-' symbol to denote a negative impact. Similarly, the number of '-' signs can range from one ('-') to three ('---') based on the severity of the negative impact.

3. Prioritize facts that could influence the stock price over the long term.

4. Evaluate the facts based on both the quantitative (impact strengths) and qualitative (relevance and importance) aspects of each fact.

5. Combine and analyze all the selected facts to predict the likely direction of the stock price movement.

Your response must be formatted as follows:

Selected Facts with Assigned Strength:
   - Fact [number] | [Content]: [Assigned Strength]
   ...
   (Include between 6-10 facts with their assigned strengths)

Decision: [Choose one: Strongly Buy, Buy, Hold, Sell, Strongly Sell. Please note that no other responses will be considered valid.]

Justification: [Provide a concise paragraph summarizing your reasoning, focusing on key facts that influence your decision.]

Fact Table: 
{fact_table}
"""


REFLECT_INSTRUCTION_less = """
You are an advanced reasoning agent capable of enhancing your capabilities through self-reflection. In a previous task, you analyzed a fact table related to a specific stock. You selected various facts from the table, assigned impacts and strengths to them, and formulated a stock investment decision along with supporting justifications. Unfortunately, your assessments led to an incorrect stock investment decision.

Your current task is to critically review your prior efforts. You must reexamine the original fact table, the facts you previously selected, the strengths you assigned to each, and the reasoning behind your conclusions. It is essential to identify significant flaws in your selection of facts (3 to 6 facts), the assignment of their strengths (1 to 3 symbols), or in the reasoning process you employed.

You must adhere to the following format in your analysis and only present the new OUTPUT part. Any deviation from this format will render it invalid. Your new stock investment decision should differ from all previous ones and should be derived exclusively from a detailed analysis of the provided facts, without relying on any pre-existing patterns.

========
INPUT:

Fact Table: 
[The full fact table will be provided here]

Previous Incorrect Outputs: 
[A list of previously incorrect outputs will be included here, containing selected facts, their assessed strengths, decisions, and the justifications provided for them.]

OUTPUT:

Selected Facts with Assigned Strength:
- Fact [number] | [Content]: [Assigned Strength]
- [This pattern will continue for each of the selected facts, ensuring that 6-10 facts are chosen.]

Decision: [Your new decision, which must be different from all previous decisions, will be one of the following: Strongly Buy, Buy, Hold, Sell, Strongly Sell.]

Justification:
[Provide a clear explanation for your updated changes and new decision in a single paragraph. Emphasize how your analysis of the facts led you to a different decision from previous outputs, and how you have addressed any errors found in prior assessments.]

========
INPUT: 

Fact Table:
{fact_table}

Previous Incorrect Outputs: The following list includes outputs from previous trials. This includes decisions that were incorrect, potentially incorrect facts that were selected, and inaccurately assigned strengths.
{previous_incorrect_outputs}

OUTPUT:
"""

PREDICT_INSTRUCTION_more = """Your task is to make an investment decision by predicting the post-earnings stock movement trend for {ticker} over a 30-day period. Use the provided fact table and follow these steps:

1. Choose 10-15 of the most relevant facts from the table. Make sure there is a balance between positive and negative facts.

2. Each selected fact needs to be assessed for its likely impact on the stock's price:
   - Use a '+' symbol to denote a positive impact. The number of '+' symbols can vary from one ('+') to three ('+++') depending on the increasing strength of the positive impact.
   - Use a '-' symbol to denote a negative impact. Similarly, the number of '-' signs can range from one ('-') to three ('---') based on the severity of the negative impact.

3. Prioritize facts that could influence the stock price over the long term.

4. Evaluate the facts based on both the quantitative (impact strengths) and qualitative (relevance and importance) aspects of each fact.

5. Combine and analyze all the selected facts to predict the likely direction of the stock price movement.

Your response must be formatted as follows:

Selected Facts with Assigned Strength:
   - Fact [number] | [Content]: [Assigned Strength]
   ...
   (Include between 6-10 facts with their assigned strengths)

Decision: [Choose one: Strongly Buy, Buy, Hold, Sell, Strongly Sell. Please note that no other responses will be considered valid.]

Justification: [Provide a concise paragraph summarizing your reasoning, focusing on key facts that influence your decision.]

Fact Table: 
{fact_table}
"""


REFLECT_INSTRUCTION_more = """
You are an advanced reasoning agent capable of enhancing your capabilities through self-reflection. In a previous task, you analyzed a fact table related to a specific stock. You selected various facts from the table, assigned impacts and strengths to them, and formulated a stock investment decision along with supporting justifications. Unfortunately, your assessments led to an incorrect stock investment decision.

Your current task is to critically review your prior efforts. You must reexamine the original fact table, the facts you previously selected, the strengths you assigned to each, and the reasoning behind your conclusions. It is essential to identify significant flaws in your selection of facts (10 to 15 facts), the assignment of their strengths (1 to 3 symbols), or in the reasoning process you employed.

You must adhere to the following format in your analysis and only present the new OUTPUT part. Any deviation from this format will render it invalid. Your new stock investment decision should differ from all previous ones and should be derived exclusively from a detailed analysis of the provided facts, without relying on any pre-existing patterns.

========
INPUT:

Fact Table: 
[The full fact table will be provided here]

Previous Incorrect Outputs: 
[A list of previously incorrect outputs will be included here, containing selected facts, their assessed strengths, decisions, and the justifications provided for them.]

OUTPUT:

Selected Facts with Assigned Strength:
- Fact [number] | [Content]: [Assigned Strength]
- [This pattern will continue for each of the selected facts, ensuring that 6-10 facts are chosen.]

Decision: [Your new decision, which must be different from all previous decisions, will be one of the following: Strongly Buy, Buy, Hold, Sell, Strongly Sell.]

Justification:
[Provide a clear explanation for your updated changes and new decision in a single paragraph. Emphasize how your analysis of the facts led you to a different decision from previous outputs, and how you have addressed any errors found in prior assessments.]

========
INPUT: 

Fact Table:
{fact_table}

Previous Incorrect Outputs: The following list includes outputs from previous trials. This includes decisions that were incorrect, potentially incorrect facts that were selected, and inaccurately assigned strengths.
{previous_incorrect_outputs}

OUTPUT:
"""

PREDICT_INSTRUCTION_transcripts = """Your task is to make an investment decision by predicting the post-earnings stock movement trend for {ticker} over a 30-day period. Use the provided earnings call transcript and follow these steps:

1. Choose 6-10 of the most relevant facts from the transcript. Make sure there is a balance between positive and negative facts.

2. Each selected fact needs to be assessed for its likely impact on the stock's price:
   - Use a '+' symbol to denote a positive impact. The number of '+' symbols can vary from one ('+') to three ('+++') depending on the increasing strength of the positive impact.
   - Use a '-' symbol to denote a negative impact. Similarly, the number of '-' signs can range from one ('-') to three ('---') based on the severity of the negative impact.

3. Prioritize facts that could influence the stock price over the long term.

4. Evaluate the facts based on both the quantitative (impact strengths) and qualitative (relevance and importance) aspects of each fact.

5. Combine and analyze all the selected facts to predict the likely direction of the stock price movement.

Your response must be formatted as follows:

Selected Facts with Assigned Strength:
   - Fact [number] | [Content]: [Assigned Strength]
   ...
   (Include between 6-10 facts with their assigned strengths)

Decision: [Choose one: Strongly Buy, Buy, Hold, Sell, Strongly Sell. Please note that no other responses will be considered valid.]

Justification: [Provide a concise paragraph summarizing your reasoning, focusing on key facts that influence your decision.]

Earnings Call Transcript: 
{fact_table}
"""

PREDICT_INSTRUCTION_comparison = """Your task is to make an investment decision by predicting the post-earnings stock movement trend for {ticker} over a 30-day period. Use the provided fact table and facts selected from the table and follow these steps:

1. Each selected fact is assessed for its likely impact on the stock's price:
   - A '+' symbol denotes a positive impact. The number of '+' symbols can vary from one ('+') to three ('+++') depending on the increasing strength of the positive impact.
   - A '-' symbol denotes a negative impact. Similarly, the number of '-' signs can range from one ('-') to three ('---') based on the severity of the negative impact.

2. Prioritize facts that could influence the stock price over the long term.

3. Evaluate the facts based on both the quantitative (impact strengths) and qualitative (relevance and importance) aspects of each fact.

4. Combine and analyze all the selected facts to predict the likely direction of the stock price movement.

Your response must be formatted as follows:

Decision: [Choose one: Strongly Buy, Buy, Hold, Sell, Strongly Sell. Please note that no other responses will be considered valid.]

Justification: [Provide a concise paragraph summarizing your reasoning, focusing on key facts that influence your decision.]

Fact Table: 
{fact_table}

{facts}
"""
