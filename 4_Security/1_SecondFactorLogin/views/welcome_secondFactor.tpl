    % include('header.tpl')

    <div class="connection-box-wrap">
        <div class="connection-box">

            <h1>Welcome {{ user['name'] }}!!!</h1>

            <p>
                Do you want to protect your account?<br />
                Register your <strong>second factor authentication</strong>!!!
            </p>

            <img src="{{qrcode}}" /><br />
                
            <a href="/login_totp" class="form-input-submit">Login</a>
 
            <p>
            	More options on your account
            </p>

            <ul>
            	<li>
            		<a href="/change_password">Change password</a>
            	</li>
            </ul>
        </div>
    </div>

    % include('footer.tpl')