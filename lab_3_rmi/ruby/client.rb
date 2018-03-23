require 'drb/drb'

def calculate(a, b, operator, operations)
	case operator
		when '+'
			operations.sum(a, b)
		when '-'
			operations.sub(a, b)
		when '/'
			if b != 0
				operations.div(a, b)
			else
				puts "Can't divide by 0"
			end
		when '*'
			operations.mult(a, b)
		else
			puts 'Invalid operation'
	end
end

DRb.start_service

ip, port = ARGV

while true do
	operations = DRbObject.new_with_uri("druby://#{ip}:#{port}")

	puts "Insert the operation on the format: 1 + 2. Put 0 0 0 to stop."
	a, operator, b = STDIN.gets.chomp.split
	a, b = a.to_i, b.to_i

	if not (a == 0 and b == 0 and operator == '0')
		puts calculate(a, b, operator, operations)
	else
		puts "Exiting..."
		break
	end
	puts
end
