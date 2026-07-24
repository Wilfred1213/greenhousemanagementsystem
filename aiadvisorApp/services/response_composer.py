class ResponseComposer:
    
    @staticmethod
    def compose(question, evidence):

        if not evidence:

            return (
                "I'm sorry, I couldn't find enough information "
                "to answer that question."
            )

        responses = []

        for item in evidence:

            tool = item.get("tool")

            data = item.get("data", {})

            if tool == "harvest":

                responses.append(
                    f"""
                🌾 Harvest Summary

                Crop : {data.get("crop")}

                Greenhouse : {data.get("greenhouse")}

                Total Harvest : {data.get("quantity_kg"):.2f} kg
                """
                                )
            elif tool == "analysis":
    
                analysis = data.get("analysis")

                if analysis == "highest_crop":

                    responses.append(
                        f"""
                    🏆 Highest Harvest Crop

                    {data["crop"]}

                    Total Harvest

                    {data["quantity_kg"]:.2f} kg
                    """
                            )

                elif analysis == "lowest_crop":

                    responses.append(
                        f"""
            📉 Lowest Harvest Crop

            {data["crop"]}

            Total Harvest

            {data["quantity_kg"]:.2f} kg
            """
                    )

                elif analysis == "highest_greenhouse":

                    responses.append(
                        f"""
            🏆 Best Performing Greenhouse

            {data["greenhouse"]}

            Total Harvest

            {data["quantity_kg"]:.2f} kg
            """
                    )

        return "\n\n".join(responses)