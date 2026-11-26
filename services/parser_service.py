import re
from difflib import get_close_matches


class ParserService:

    @staticmethod
    def detect_chart_type(prompt: str):

        prompt = prompt.lower()

        chart_keywords = {
            "bar": ["bar", "column"],
            "line": ["line"],
            "scatter": ["scatter"],
            "pie": ["pie"],
            "histogram": ["histogram", "distribution"]
        }

        for chart_type, keywords in chart_keywords.items():
            for keyword in keywords:
                if keyword in prompt:
                    return chart_type

        return "bar"

    @staticmethod
    def detect_aggregation(prompt: str):

        prompt = prompt.lower()

        if any(word in prompt for word in ["average", "avg", "mean"]):
            return "mean"

        if any(word in prompt for word in ["sum", "total"]):
            return "sum"

        if "count" in prompt:
            return "count"

        return None

    @staticmethod
    def normalize(text: str):
        """
        Convert text to lowercase and remove punctuation.
        """
        text = text.lower()
        text = re.sub(r"[^a-z0-9\s]", "", text)
        return text

    @staticmethod
    def detect_axes(prompt: str, columns: list):

        normalized_prompt = ParserService.normalize(prompt)

        matched_columns = []

        # Exact Match
        for column in columns:
            normalized_column = ParserService.normalize(column)

            if normalized_column in normalized_prompt:
                matched_columns.append(column)

        # Fuzzy Match
        if len(matched_columns) < 2:

            words = normalized_prompt.split()

            for word in words:

                match = get_close_matches(
                    word,
                    columns,
                    n=1,
                    cutoff=0.8
                )

                if match:

                    if match[0] not in matched_columns:
                        matched_columns.append(match[0])

        x_axis = None
        y_axis = None

        prompt_lower = normalized_prompt

        if " by " in prompt_lower and len(matched_columns) >= 2:

            before_by = prompt_lower.split(" by ")[0]
            after_by = prompt_lower.split(" by ")[1]

            for column in matched_columns:

                normalized_column = ParserService.normalize(column)

                if normalized_column in before_by:
                    y_axis = column

                if normalized_column in after_by:
                    x_axis = column

        elif " against " in prompt_lower and len(matched_columns) >= 2:

            before = prompt_lower.split(" against ")[0]
            after = prompt_lower.split(" against ")[1]

            for column in matched_columns:

                normalized_column = ParserService.normalize(column)

                if normalized_column in before:
                    y_axis = column

                if normalized_column in after:
                    x_axis = column

        elif " vs " in prompt_lower and len(matched_columns) >= 2:

            before = prompt_lower.split(" vs ")[0]
            after = prompt_lower.split(" vs ")[1]

            for column in matched_columns:

                normalized_column = ParserService.normalize(column)

                if normalized_column in before:
                    y_axis = column

                if normalized_column in after:
                    x_axis = column

        elif len(matched_columns) >= 2:

            y_axis = matched_columns[0]
            x_axis = matched_columns[1]

        elif len(matched_columns) == 1:

            x_axis = matched_columns[0]

        return x_axis, y_axis

    @staticmethod
    def parse_prompt(prompt: str, columns: list):

        chart_type = ParserService.detect_chart_type(prompt)

        aggregation = ParserService.detect_aggregation(prompt)

        x_axis, y_axis = ParserService.detect_axes(
            prompt,
            columns
        )

        return {
            "original_prompt": prompt,
            "chart_type": chart_type,
            "x_axis": x_axis,
            "y_axis": y_axis,
            "aggregation": aggregation
}