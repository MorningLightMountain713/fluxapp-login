# Flux App Login Example

## Requirements

uv - https://docs.astral.sh/uv/getting-started/installation/

## Install

```bash
uv sync
```

## Usage

```
> flux-login
Login Response:

{
│   'status': 'success',
│   'data': {
│   │   'message': 'Successfully logged in',
│   │   'zelid': '1HQjz5oNpYjVzAE7FWzU8oAww1zX9XBzJ',
│   │   'loginPhrase': '17454819006886cklgfoihk6oms2abpwvaw7kro0dpqqnw1s9uq5p5a',
│   │   'signature': 'H+V3pa4RiI+hTPmsYTK0o2eHu5eqKq6p1PIND3J26vNELAJ9gHnn+AQKUys2fcTe1eyF+SAlP20RBpwVYfZkuK4=',
│   │   'privilage': 'user',
│   │   'createdAt': '2025-04-24T08:05:00.688Z',
│   │   'expireAt': '2025-05-08T08:05:00.688Z'
│   }
}

Auth header for future api calls:

{
│   'zelidauth': 'zelid=1HQjz5oNpYjVzAE7FWzU8oAww1zX9XBzJ&signature=H%2BV3pa4RiI%2BhTPmsYTK0o2eHu5eqKq6p1PIND3J26vNELAJ9gHnn%2BAQKUys2fcTe1eyF%2BSAlP20RBpwVYfZkuK4%3D&loginPhrase=17454819006886cklgfoihk6oms2abpwvaw7kro0dpqqnw1s9uq5p5a'
}
```

This will generate a new key on each login - which is not what you want. You would want to generate a key one-time, then pass in the same key in the future.

Once logged in, you can use the auth header on subsequent calls that require authentication / authorization.
