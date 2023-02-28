# SpotifyManager
I wrote this script to migrate my entire Spotify library with 2 accounts, which consisted of hundreds of playlists, albums and thousands of songs

Used OAuth 2.0 to access my accounts through the Spotify API.

To avoid having to manually transfer the authorization tokens to the application, I used a simple HTTP server I wrote earlier to handle the redirect URL after authorization at runtime.

It saves the structure and contents of the library of a specified user account, saves it into a file, and then it can be run again later to upload this data onto a new user's account.

While it was written as a single-use program, it has the functionality to have full edit control over the user's library and the possibility to be extended into a proper application.
