	% include('header.tpl')
	
	<div class="connection-box-wrap">
		<div class="connection-box">
			% if signup:
			<h1>Sign up</h1>
			<form action="/signup" method="POST">
			% else:
			<h1>Login in</h1>
			<form action="/login" method="POST">
			%end
				
				<div class="form-input"> 
					<label for="username">Your username</label>
					<input id="username" name="username" autocomplete="off" required="required" type="text" placeholder="Username" />
				</div>

				<div class="form-input"> 
					<label for="password">Your password </label> 
					<input id="password" name="password" required="required" type="password" placeholder="eg. X8df!90EO"/>
				</div>

				% if not signup:
					<div class="form-input">
						<input type="submit" class="form-input-submit" value="Connect"/>
					</div>
				% else:
					<div class="form-input"> 
						<label for="password">Retype the password</label> 
						<input id="password2" name="password2" required="required" type="password" placeholder="eg. X8df!90EO"/>
					</div>

					<div class="form-input"> 
						<label for="email">Your email</label>
						<input id="email" name="email" required="required" type="email" placeholder="mysupermail@mail.com"/> 
					</div>
					
					<div class="form-input">
						<label for="name">Your name</label>
						<input id="name" name="name" required="required" type="text" placeholder="Your name" />
					</div>

					<div class="form-input">
						<label for="country">Your country</label>
						<input id="country" name="country" required="required" type="text" placeholder="Your country" />
					</div>

					<div class="form-input">
						<input type="submit" value="Sign up"/>
					</div>
				% end

			</form>
		
			<div class="form-extraOptions">
				% if signup:
					<p> 
						Already a member ?
						<a href="/login" class="to_register"> Go and log in </a>
					</p>
				% else:
					<p> 
						Do you need an account?
						<a href="/signup" class="to_register"> Go and sign up </a>
					</p>
				% end
			</div>
			
		</div>
	</div>
	% include('footer.tpl')
