REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'src.oauth.authentication.JWTAuthentication',
    ],
}
