# To Implement
- SingleEntryPage:
    - Implement tooltip for the singleentrypage in lieu of the bracketed (Optional Desc, Free Flow, 24 HR format) infos
    - Have a toggleable/switchable button between single and session entry pages * prob do after setting up the session page
        - if the pages a swapped, make sure the previous pages entries dont get processed, and the whole thing is deleted or just erased.
- SessionEntryPage:
    * thought process
        - just reset the fields except for label (if the user has written something, as its a way for them to group the exercises together)
        - and essentially let them submit each entry with a different button OR better yet, change the way the 'add_exercise' button works
        in that it, doesnt redirect to the dashboard, just cleans, just does what the first point mentions (.ie. just reset the fields except..)
        - Have another button beside it that is the actual one that redirects home... [Go To Dashboard] <-- should probably have a tooltip indicating that it should only be pressed once all entries entered
        - Persist the entered label detail (that can be the optional but best way to indicate a grouped session entry)
        - So, if the form has unsaved input (like they typed reps or weight but didn’t press submit), then:
            ✅ You could show a popup:

                "You have unsaved input. Make sure to press Submit for each exercise before finishing your session."
        

    ** IMPORTANT BELOW **
    - remove the column and row configures for the grid layout that have a weight of 0, as that is a default setting so redundant to explicitly write out.
    - fix naming convention in the 'return_to_dashboard' function in the SessionEntryPage
    - assess whether theres a more proper way than copying majority of code from SingleEntryPage to SessionEntryPage
    - add comments to the return_to_dashboard() function in the SessionEntryPage
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

