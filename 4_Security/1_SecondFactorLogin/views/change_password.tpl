% include('header.tpl')

<div class="connection-box-wrap">
    <div class="connection-box">

        <form action="/change_password" method="POST">
			
			<h1>Change password</h1>

        	<div class="form-input"> 
        		<label for="username">Your username</label>
        		<input id="username" name="username" autocomplete="off" required="required" type="text" placeholder="Username" />
        	</div>
        	
        	<div class="form-input"> 
        		<label for="oldpassword">Old password</label>
        		<input id="oldpassword" name="oldpassword" autocomplete="off" required="required" type="password" placeholder="Your old password" />
        	</div>
        	
        	<div class="form-input"> 
        		<label for="newpassword">New password</label>
        		<input id="newpassword" name="newpassword" autocomplete="off" required="required" type="password" placeholder="Your new password" />
        	</div>

			 <div class="form-input">
			 	<input type="submit" class="form-input-submit form-input-change" value="Change!"/>
			 </div>

        </form>

    </div>
</div>

% include('footer.tpl')


 