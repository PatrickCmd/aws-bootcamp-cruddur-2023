-- this file was manually created
INSERT INTO public.users (display_name, handle, email, cognito_user_id)
VALUES
  ('Andrew Brown', 'andrewbrown', 'andrewbrown@cloudprojectbootcamp.com', 'MOCK'),
  ('Andrew Bayko', 'bayko', 'bayko@cloudprojectbootcamp.com', 'MOCK'),
  ('Patrick Walukagga', 'patrickcmd', 'pwalukagga@gmail.com', 'MOCK'),
  ('Telnet Cmd', 'telnetcmd', 'patrickcmdtelnet@gmail.com', 'MOCK');

INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES
  (
    (SELECT uuid from public.users WHERE users.handle = 'patrickcmd' LIMIT 1),
    'This was imported as seed data!',
    current_timestamp + interval '10 day'
  )