# Learning why things work the way they work

- self is the root window that is the container for container and container is the container for all the pages (child classes)
- the container stacks the pages ontop of each other, and we use the tkraise() to decide which one to put at the top, cause the top is the one that gets displayed.
- The pattern being used: 
self (Window)
└── container (Frame)
    └── multiple pages (frames)
- the self only requires grid configuration for 1 row and column because its only taking in 1 widget, which is the container frame
- the container also only requires grid configuration for 1 row and column because it also is only taking in a widget at a time (per page)
- usage of hasattr or isinstance is better than 'selected_page == RegisterPage' because its less hardcoded and its checking instances rather than classes
- hasattr or isinstance... reduces tight coupling?
- Using stuff like 'NOT NULL' and 'FOREIGN KEY xx REFERENCES xx' are great ways to ensure there is no database corruptions / last line of defence (esp for usage of NOT NULL)