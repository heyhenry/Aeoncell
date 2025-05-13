
## SHOULD DO NEXT 
- add padding and styling to the base entry page in reference to the form and the popup box.

# To Implement
- Implement tooltip for the singleentrypage in lieu of the bracketed (Optional Desc, Free Flow, 24 HR format) infos
- Have a toggleable/switchable button between single and session entry pages * prob do after setting up the session page
    - if the pages a swapped, make sure the previous pages entries dont get processed, and the whole thing is deleted or just erased.


    ** WHEN IMPLEMENTING THE SWITCH BUTTON BETWEEN SINGLE AND SESSION PAGES **
        - ensure to implement the popup confirmation box for both pages upon switching whilst there is content in the entry


# To Consider
- Address invalid step tracker user input 
    - Probably just don't update or proceed with any logic if the input is invalid
        - No point in dropping an error message.. its prety intuitive to understand you need to just enter digits
- Mistake correction feature for the step tracker daily steps (i.e. edit steps.)
    - Alternatively, offer a clear_steps button instead
        - Confirmation dialog popup "Are you sure you want to clear today's steps?"
        - Only show the clear button if the total steps are over 0? (meh probably not, keep a consistent ui visual)
        - Visually it could be an undo icon, smaller than the add button, and maybe top right of the section box?

