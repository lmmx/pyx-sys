# TODO

- I want to be able to `STOP` (i.e. pause) processes to prevent them getting CPU time,
  i.e. to enforce backgrounding of idle processes
  - This is motivated by regularly seeing 5% and upwards being churned over on CPU
    by "Web Content" processes [anonymous processes belonging to Firefox], even
    when I am not browsing the web. At best this is wasteful, at worst it could be
    someone exploiting my hardware for bitcoin mining etc. etc. (I doubt it but I also
    want to prevent anything of that sort from being possible).
  - To do this I must use the constructed process tree to pause the parent window
    as pausing the "Web Content" process itself does nothing.
  - To further aid this, I want to introduce LXD containers into this workflow
- Add LXD interaction at first via command line passing, but ideally via its Python
  interface, then control their containerised processes on the host windowing system.
