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
    
            print("=" * 50)
            print("RESPONSE COMPOSER ITEM")
            print(item)

        for item in evidence:

            # Old-style tool
            if isinstance(item, str):
                responses.append(item)
                continue

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
                elif analysis == "lowest_greenhouse":
    
                    responses.append(
                        f"""
                📉 Lowest Producing Greenhouse

                {data["greenhouse"]}

                Total Harvest

                {data["quantity_kg"]:.2f} kg
                """
                    )
            elif tool == "farm":
    
                knowledge = data.get("knowledge")
                if knowledge == "current_crop":
    
                    responses.append(
                        f"""
                🌱 Current Crops

                {chr(10).join(data["crops"])}

                Active Crops: {data["count"]}
                """
                    )

            elif tool == "farm_status":
    
                knowledge = data.get("knowledge")

                if knowledge == "greenhouse_summary":

                    responses.append(

                    f"""
                    🏡 {data["greenhouse"]}

                    Current Crop
                    ------------
                    {data["crop"]}

                    Current Stage
                    -------------
                    {data["status"]}

                    Production Cycle
                    ----------------
                    {data["cycle"]}

                    Season
                    ------
                    {data["season"]}

                    Transplanted
                    ------------
                    {data["transplant_date"]}

                    Expected First Harvest
                    ----------------------
                    {data["next_harvest"]}

                    Beds Occupied
                    -------------
                    {data["beds"]}

                    Total Harvest
                    -------------
                    {data["harvest"]:.2f} kg
                    """
                            )
                elif knowledge == "greenhouse_occupancy":
    
                    responses.append(
                        f"""
                🏡 Most Occupied Greenhouse

                Greenhouse
                ----------
                {data["greenhouse"]}

                Occupied Beds
                -------------
                {data["occupied_beds"]}
                """
                    )

            elif tool == "production_cycle":
    
                info = data.get("production")

                if info == "transplant_date":

                    responses.append(
                        f"""
            🌱 Transplant Information

            Crop:
            {data["crop"]}

            Actual Transplant Date:
            {data["date"]}
            """
                    )

                elif info == "next_harvest":

                    responses.append(
                        f"""
            🧺 Next Expected Harvest

            Crop:
            {data["crop"]}

            Greenhouse:
            {data["greenhouse"]}

            Expected Harvest Date:
            {data["date"]}
            """
                    )

                elif info == "crop_stage":

                    responses.append(
                        f"""
            🌱 Crop Status

            Crop:
            {data["crop"]}

            Current Stage:
            {data["stage"]}
            """
                    )

                elif info == "ready_harvest":

                    text = ""

                    for item in data["harvests"]:
                        text += f"• {item['crop']} ({item['greenhouse']})\n"

                    responses.append(
                        f"""
            🧺 Crops Ready For Harvest

            {text}
            """
                    )
            elif tool == "gemini":
        
                responses.append(data["answer"])
            
        return "\n\n".join(responses)