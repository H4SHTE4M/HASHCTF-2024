package route

import (
	"fmt"
	"github.com/flosch/pongo2/v6"
	"github.com/gin-gonic/gin"
	"github.com/gorilla/sessions"
	"html"
	"html/template"
	"net/http"
	"os"
)

type SuperCTFer struct {
	name   string
	skill  string
	secret []byte
}

var store = sessions.NewCookieStore([]byte(os.Getenv("SESSION_KEY")))

func Index(c *gin.Context) {
	session, err := store.Get(c.Request, "session-name")
	if err != nil {
		http.Error(c.Writer, err.Error(), http.StatusInternalServerError)
		return
	}
	if session.Values["name"] == nil {
		session.Values["name"] = "guest"
		err = session.Save(c.Request, c.Writer)
		if err != nil {
			http.Error(c.Writer, err.Error(), http.StatusInternalServerError)
			return
		}
	}

	c.String(200, "oh, guest? a ring of play!")
}

func Welcome(c *gin.Context) {
	session, err := store.Get(c.Request, "session-name")
	if err != nil {
		http.Error(c.Writer, err.Error(), http.StatusInternalServerError)
		return
	}
	if session.Values["name"] == nil {
		session.Values["name"] = "guest"
		err = session.Save(c.Request, c.Writer)
		if err != nil {
			http.Error(c.Writer, err.Error(), http.StatusInternalServerError)
			return
		}
	}

	ctf := &SuperCTFer{"", "", []byte(os.Getenv("SESSION_KEY"))}
	ctf.name = c.Param("username")
	ctf.skill = "web"

	if ctf.name == "" {
		ctf.name = "hacker"
	}

	tmpl := fmt.Sprintf(`<!DOCTYPE html>
<html>
<head>
    <title>Welcome</title>
    <style>
        body {
            background-color: #f2f2f2;
            font-family: Arial, sans-serif;
            text-align: center;
        }

        .welcome-container {
            background-color: #ffffff;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            padding: 40px;
            margin: 100px auto;
            max-width: 400px;
        }

        h1 {
            color: #333333;
            font-size: 28px;
            margin-bottom: 20px;
        }

        p {
            color: #666666;
            font-size: 18px;
            line-height: 1.5;
        }
    </style>
</head>
<body>
<div class="welcome-container">
    <h1>Welcome to ` + ctf.name + `! <br/>You focus on ` + ctf.skill + ` Security </h1>
    <p>enjoy your hacking</p>
</div>
</body>
</html>`)
	html, err := template.New("welcome").Parse(tmpl)
	html = template.Must(html, err)
	err = html.Execute(c.Writer, ctf)
	if err != nil {
		c.String(500, "oh no!", nil)
	}
	c.String(200, "")
}

func Admin(c *gin.Context) {
	session, err := store.Get(c.Request, "session-name")
	if err != nil {
		http.Error(c.Writer, err.Error(), http.StatusInternalServerError)
		return
	}
	if session.Values["name"] != "admin" {
		http.Error(c.Writer, "No! admin plz.", http.StatusInternalServerError)
		return
	}
	name := c.DefaultQuery("name", "ssti")
	xssWaf := html.EscapeString(name)
	tpl, err := pongo2.FromString("Hello " + xssWaf + "!")
	if err != nil {
		panic(err)
	}
	out, err := tpl.Execute(pongo2.Context{"c": c})
	if err != nil {
		http.Error(c.Writer, err.Error(), http.StatusInternalServerError)
		return
	}
	c.String(200, out)
}
