
# priority thought
- unsatisfied with the design outcome of the register page... how to improve..?
    - opt for the usage of an overflowing and engaging cover image that doesn't have a straight divide (i.e. cloud style)
    - potentially opt for an image as a frame rather than the simple rectangle backdrop for the form
        - but frames dont have an image attribute..
            - so maybe a label widget will hold an image that encompasses the form's frame?
            - or utilising the canvas widget?
            - or not using a frame at all?
- colour scheme uncertainty..
    - best to choose one from the custom ctk themes and work on the project and alter colour palette later if need be
    - or create a brand new customised colour scheme..
        - but tkinter, or atleast customtkinter does not accept gradient colours..
            - loop back to the initial solution proposal?

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

