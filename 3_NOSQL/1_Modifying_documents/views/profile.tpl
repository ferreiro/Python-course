% include('header.tpl')

<h1>
	@{{user['_id']}} profile
</h1>

%for key in user:
	% if key == 'likes':
		<p>
			<b>Tags:</b>
			%for l in user[key]:
				<span class="tag">
					{{l}}
				</span>
			%end
		</p>
	% elif key == 'address':
		<p>
			<b>Address:</b>
			%for l in user[key]:
				<span class="tag">
					{{user[key][l]}}
				</span>
			%end
		</p>
	% else:
		<p> {{key}}: {{user[key]}}</p>
	% end 
% end