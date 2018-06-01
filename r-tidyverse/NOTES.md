At some point, we might wan to include Docker snippets like the below to
facilitate industry MS SQL usage:

```{Dockerfile}
# Get MS SQL files and other development needs for SQL Server ODBC in R
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    # Rocker's stable branch is based on Debian stretch / 9
    curl https://packages.microsoft.com/config/debian/9/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update -qq && \
    ACCEPT_EULA=Y apt-get install -y --no-install-recommends unixodbc-dev msodbcsql17 odbc-postgresql
    # Actaully, it looks like I can just use the MS driver directly
    # but these packages let us build RSQLServer: openjdk-8-headless liblzma-dev libbz2-dev
    # liblzma and libbz2 are also required to build rJava, which is a dep of RSQLServer

RUN install2.r --error --deps TRUE odbc pool
```

We should probably use install2.r for non-conda R package installation

R is compiled against some X libraries. The absolute necessary items are
addressed by apt-installing libxrender1 and libxext6, but I still see the
`R_X11.so` / `libSM.so.6` warnings if I run from the console.
