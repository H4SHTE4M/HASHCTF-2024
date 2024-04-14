package main

import (
	"github.com/gin-gonic/gin"
	"main/route"
	"os"
)

func main() {
	//I don't tell you the session key, can you find it?
	//err := os.Setenv("SESSION_KEY", "fake_session_key")
	err := os.Setenv("SESSION_KEY", "th1s_1s_w3b_g0_ch4l1eng3")
	if err != nil {
		return
	}
	r := gin.Default()
	r.GET("/", route.Index)
	r.GET("/welcome", route.Welcome)
	r.GET("/welcome/:username", route.Welcome)
	r.GET("/admin", route.Admin)

	err = r.Run("0.0.0.0:80")
	if err != nil {
		return
	}

}
