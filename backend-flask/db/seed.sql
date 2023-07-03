-- this file was manually created
INSERT INTO public.users (display_name, handle, email, cognito_user_id)
VALUES
  ('Patrick Walukagga', 'patrickcmd', 'pwalukagga@gmail.com', 'MOCK'),
  ('Telnet Cmd', 'patrickcmdtelnet', 'patrickcmdtelnet@gmail.com', 'MOCK'),
  ('Patrick Rickson', 'patrickcmd101', 'patrick.walukagga@audersity.com', 'MOCK'),
  ('Andrew Brown', 'andrewbrown', 'andrewbrown@cloudprojectbootcamp.com', 'MOCK'),
  ('Andrew Bayko', 'bayko', 'bayko@cloudprojectbootcamp.com', 'MOCK'),
  ('Londo Mollari','lmollari@centari.com' ,'londo' ,'MOCK');

INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES
  (
    (SELECT uuid from public.users WHERE users.handle = 'patrickcmd' LIMIT 1),
    'This was imported as seed data!',
    current_timestamp + interval '10 day'
  )