# To check test and sus
- Check if a new entry is created tomorrow (23rd April) while the previous one is maintained
- Make sure that the new entry is clean and doesnt have yesterdays steps 
- Make sure yesterday's steps cant get manipulated/edited/changed when the day is different

# To Implement
- Implement the collapsible ive created in -> collapse.py into the main.py
- Address invalid step tracker user input 
    - Probably just don't update or proceed with any logic if the input is invalid
        - No point in dropping an error message.. its prety intuitive to understand you need to just enter digits

# To Consider
- Mistake correction feature for the step tracker daily steps (i.e. edit steps.)
    - Alternatively, offer a clear_steps button instead
        - Confirmation dialog popup "Are you sure you want to clear today's steps?"
        - Only show the clear button if the total steps are over 0? (meh probably not, keep a consistent ui visual)
        - Visually it could be an undo icon, smaller than the add button, and maybe top right of the section box?